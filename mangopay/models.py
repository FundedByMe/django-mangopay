import urllib2
import base64
import jsonfield
from datetime import datetime
from decimal import Decimal, ROUND_FLOOR

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.db import models
from django.utils.timezone import utc

from money.contrib.django.models.fields import MoneyField
from model_utils.managers import InheritanceManager
from mangopaysdk.entities.usernatural import UserNatural
from mangopaysdk.entities.userlegal import UserLegal
from mangopaysdk.entities.bankaccount import BankAccount
from mangopaysdk.entities.kycdocument import KycDocument
from mangopaysdk.entities.wallet import Wallet
from mangopaysdk.entities.kycpage import KycPage
from mangopaysdk.entities.payout import PayOut
from mangopaysdk.entities.payin import PayIn
from mangopaysdk.entities.refund import Refund
from mangopaysdk.entities.transfer import Transfer
from mangopaysdk.entities.cardregistration import CardRegistration
from mangopaysdk.types.money import Money
from mangopaysdk.types.bankaccountdetailsiban import BankAccountDetailsIBAN
from mangopaysdk.types.bankaccountdetailsus import BankAccountDetailsUS
from mangopaysdk.types.bankaccountdetailsother import BankAccountDetailsOTHER

from mangopaysdk.types.payoutpaymentdetailsbankwire import (
    PayOutPaymentDetailsBankWire)
from mangopaysdk.types.payinpaymentdetailsbankwire import (
    PayInPaymentDetailsBankWire)
from mangopaysdk.types.payinexecutiondetailsdirect import (
    PayInExecutionDetailsDirect)
from mangopaysdk.types.payinpaymentdetailscard import PayInPaymentDetailsCard
from django_countries.fields import CountryField

from localflavor.generic.models import IBANField, BICField
from money import Money as PythonMoney

import django_filepicker

from .constants import (INCOME_RANGE_CHOICES,
                        STATUS_CHOICES, DOCUMENT_TYPE_CHOICES,
                        CREATED, STATUS_CHOICES_DICT, NATURAL_USER,
                        DOCUMENT_TYPE_CHOICES_DICT, USER_TYPE_CHOICES,
                        VALIDATED, IDENTITY_PROOF, VALIDATION_ASKED,
                        REGISTRATION_PROOF, ARTICLES_OF_ASSOCIATION,
                        SHAREHOLDER_DECLARATION, TRANSACTION_STATUS_CHOICES,
                        REFUSED, BUSINESS, ORGANIZATION,
                        USER_TYPE_CHOICES_DICT,
                        MANGOPAY_BANKACCOUNT_TYPE, BANK_WIRE, CARD_WEB,
                        BA_BIC_IBAN, BA_US, BA_OTHER,
                        BA_US_DEPOSIT_ACCOUNT_TYPES,
                        BA_NOT_IMPLEMENTED, MANGOPAY_PAYIN_CHOICES)

from .client import get_mangopay_api_client


auth_user_model = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


def python_money_to_mangopay_money(python_money):
    amount = python_money.amount.quantize(Decimal('.01'),
                                          rounding=ROUND_FLOOR) * 100
    return Money(amount=int(amount), currency=str(python_money.currency))


def get_execution_date_as_datetime(mangopay_entity):
    execution_date = mangopay_entity.ExecutionDate
    if execution_date:
        formated_date = datetime.fromtimestamp(int(execution_date))
        if settings.USE_TZ:
            return formated_date.replace(tzinfo=utc)
        else:
            return formated_date


class MangoPayUser(models.Model):
    objects = InheritanceManager()

    create_timestamp = models.DateTimeField(auto_now_add=True, null=True)
    last_edit_timestamp = models.DateTimeField(auto_now=True, null=True)

    mangopay_id = models.PositiveIntegerField(null=True, blank=True)
    user = models.ForeignKey(auth_user_model, related_name="mangopay_users")
    type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES,
                            null=True)
    first_name = models.CharField(null=True, blank=True, max_length=99)
    last_name = models.CharField(null=True, blank=True, max_length=99)
    email = models.EmailField(max_length=254, blank=True, null=True)

    # Light Authentication Field:
    birthday = models.DateField(blank=True, null=True)
    country_of_residence = CountryField()
    nationality = CountryField()

    # Regular Authentication Fields:
    address = models.CharField(blank=True, null=True, max_length=254)

    def create(self):
        client = get_mangopay_api_client()
        mangopay_user = self._build()
        created_mangopay_user = client.users.Create(mangopay_user)
        self.mangopay_id = created_mangopay_user.Id
        self.save()

    def update(self):
        client = get_mangopay_api_client()
        return client.users.Update(self._build())

    def is_legal(self):
        return self.type in [BUSINESS, ORGANIZATION]

    def is_natural(self):
        return self.type == NATURAL_USER

    def has_regular_authenication(self):
        return (self.has_light_authenication()
                and self._are_required_documents_validated())

    def required_documents_types_that_need_to_be_reuploaded(self):
        return [t for t in self._required_documents_types() if
                self._document_needs_to_be_reuploaded(t)]

    def _document_needs_to_be_reuploaded(self, t):
        return (self.mangopay_documents.filter(
                type=t, status=REFUSED).exists()
                and not self.mangopay_documents.filter(
                    type=t,
                    status__in=[VALIDATED, VALIDATION_ASKED]).exists()
                and not self.mangopay_documents.filter(
                    type=t, status__isnull=True).exists())

    def _build(self):
        return NotImplementedError

    def _birthday_fmt(self):
        return int(self.birthday.strftime("%s"))

    def _are_required_documents_validated(self):
        are_validated = True
        for type in self._required_documents_types():
            are_validated = self.mangopay_documents.filter(
                type=type, status=VALIDATED).exists() and are_validated
        return are_validated

    @property
    def _first_name(self):
        if self.first_name:
            return self.first_name
        try:
            return self.user.first_name
        except AttributeError:
            pass
        return ''

    @property
    def _last_name(self):
        if self.last_name:
            return self.last_name
        try:
            return self.user.last_name
        except AttributeError:
            pass
        return ''

    @property
    def _email(self):
        if self.email:
            return self.email
        try:
            return self.user.email
        except AttributeError:
            pass
        return ''


class MangoPayNaturalUser(MangoPayUser):
    # Regular Authenication Fields:
    occupation = models.CharField(blank=True, null=True, max_length=254)
    income_range = models.SmallIntegerField(
        blank=True, null=True, choices=INCOME_RANGE_CHOICES)

    def _build(self):
        mangopay_user = UserNatural()
        mangopay_user.FirstName = self._first_name
        mangopay_user.LastName = self._last_name
        mangopay_user.Email = self._email
        mangopay_user.Birthday = self._birthday_fmt()
        mangopay_user.CountryOfResidence = self.country_of_residence.code
        mangopay_user.Nationality = self.nationality.code
        mangopay_user.Occupation = self.occupation
        mangopay_user.IncomeRange = self.income_range
        mangopay_user.Address = self.address
        mangopay_user.Id = self.mangopay_id
        return mangopay_user

    def __unicode__(self):
        return self.user.get_full_name()

    def save(self, *args, **kwargs):
        self.type = NATURAL_USER
        return super(MangoPayNaturalUser, self).save(*args, **kwargs)

    def has_light_authenication(self):
        return (self.user
                and self.country_of_residence
                and self.nationality
                and self.birthday)

    def has_regular_authenication(self):
        return (self.address
                and self.occupation
                and self.income_range
                and super(MangoPayNaturalUser,
                          self).has_regular_authenication())

    def _required_documents_types(self):
        return [IDENTITY_PROOF]


class MangoPayLegalUser(MangoPayUser):
    business_name = models.CharField(max_length=254)
    generic_business_email = models.EmailField(max_length=254)

    # Regular Authenication Fields:
    headquaters_address = models.CharField(blank=True, max_length=254,
                                           null=True)

    def _build(self):
        mangopay_user = UserLegal()
        mangopay_user.Email = self.generic_business_email
        mangopay_user.Name = self.business_name
        mangopay_user.LegalPersonType = USER_TYPE_CHOICES_DICT[self.type]
        mangopay_user.HeadquartersAddress = self.headquaters_address
        mangopay_user.LegalRepresentativeFirstName = self.first_name
        mangopay_user.LegalRepresentativeLastName = self.last_name
        mangopay_user.LegalRepresentativeAddress = self.address
        mangopay_user.LegalRepresentativeEmail = self.email
        mangopay_user.LegalRepresentativeBirthday = self._birthday_fmt()
        mangopay_user.LegalRepresentativeNationality = self.nationality.code
        mangopay_user.LegalRepresentativeCountryOfResidence =\
            self.country_of_residence.code
        mangopay_user.Id = self.mangopay_id
        return mangopay_user

    def __unicode__(self):
        if self.business_name:
            return self.business_name
        else:
            return super(MangoPayLegalUser, self).__unicode__()

    def has_light_authenication(self):
        return (self.type
                and self.business_name
                and self.generic_business_email
                and self.first_name
                and self.last_name
                and self.country_of_residence
                and self.nationality
                and self.birthday)

    def has_regular_authenication(self):
        return (self.address
                and self.headquaters_address
                and self.address
                and self.email
                and super(MangoPayLegalUser, self).has_regular_authenication())

    def _required_documents_types(self):
        types = [IDENTITY_PROOF, REGISTRATION_PROOF]
        if self.type == BUSINESS:
            types.append(SHAREHOLDER_DECLARATION)
        elif self.type == ORGANIZATION:
            types.append(ARTICLES_OF_ASSOCIATION)
        return types


class MangoPayDocument(models.Model):
    mangopay_id = models.PositiveIntegerField(null=True, blank=True)
    mangopay_user = models.ForeignKey(MangoPayUser,
                                      related_name="mangopay_documents")
    type = models.CharField(max_length=2,
                            choices=DOCUMENT_TYPE_CHOICES)
    status = models.CharField(blank=True, null=True, max_length=1,
                              choices=STATUS_CHOICES)
    refused_reason_message = models.CharField(null=True, blank=True,
                                              max_length=255)

    def create(self, tag=''):
        document = KycDocument()
        document.Tag = tag
        document.Type = DOCUMENT_TYPE_CHOICES_DICT[self.type]
        client = get_mangopay_api_client()
        created_document = client.users.CreateUserKycDocument(
            document, self.mangopay_user.mangopay_id)
        self.mangopay_id = created_document.Id
        self.status = STATUS_CHOICES_DICT[created_document.Status]
        self.save()

    def get(self):
        client = get_mangopay_api_client()
        document = client.users.GetUserKycDocument(
            self.mangopay_id, self.mangopay_user.mangopay_id)
        self.refused_reason_message = document.RefusedReasonMessage
        self.status = STATUS_CHOICES_DICT[document.Status]
        self.save()
        return self

    def ask_for_validation(self):
        if self.status == CREATED:
            document = KycDocument()
            document.Id = self.mangopay_id
            document.Status = "VALIDATION_ASKED"
            client = get_mangopay_api_client()
            updated_document = client.users.UpdateUserKycDocument(
                document, self.mangopay_user.mangopay_id, self.mangopay_id)
            self.status = STATUS_CHOICES_DICT[updated_document.Status]
            self.save()
        else:
            raise BaseException('Cannot ask for validation of a document'
                                'not in the created state')

    def __unicode__(self):
        return str(self.mangopay_id) + " " + str(self.status)


def page_storage():
    if settings.MANGOPAY_PAGE_DEFAULT_STORAGE:
        return default_storage
    else:
        from storages.backends.s3boto import S3BotoStorage
        return S3BotoStorage(
            acl='private',
            headers={'Content-Disposition': 'attachment',
                     'X-Robots-Tag': 'noindex, nofollow, noimageindex'},
            bucket=settings.AWS_MEDIA_BUCKET_NAME,
            custom_domain=settings.AWS_MEDIA_CUSTOM_DOMAIN)


class MangoPayPage(models.Model):
    document = models.ForeignKey(MangoPayDocument,
                                 related_name="mangopay_pages")
    file = django_filepicker.models.FPUrlField(
        max_length=255,
        additional_params={
            'data-fp-store-path': 'mangopay_pages/',
            'data-fp-store-location': 'S3',
        })

    def create(self):
        page = KycPage()
        page.File = self._file_bytes().decode("utf-8")
        client = get_mangopay_api_client()
        client.users.CreateUserKycPage(page,
                                       self.document.mangopay_user.mangopay_id,
                                       self.document.mangopay_id)

    def _file_bytes(self):
        response = urllib2.urlopen(self.file)
        bytes = base64.b64encode(response.read())
        return bytes


class MangoPayBankAccount(models.Model):
    mangopay_user = models.ForeignKey(MangoPayUser,
                                      related_name="mangopay_bank_accounts")
    mangopay_id = models.PositiveIntegerField(null=True, blank=True)

    address = models.CharField(max_length=254)
    account_type = models.CharField(max_length=2,
                                    choices=MANGOPAY_BANKACCOUNT_TYPE,
                                    default=BA_BIC_IBAN)  # Defaults to BIC/IBAN type

    iban = IBANField(blank=True, null=True)

    bic = BICField(blank=True, null=True)
    country = CountryField(null=True, blank=True)
    account_number = models.CharField(max_length=15, null=True, blank=True)

    # BA_US type only fields
    aba = models.CharField(max_length=9, null=True, blank=True)
    deposit_account_type = models.CharField(
        choices=BA_US_DEPOSIT_ACCOUNT_TYPES,
        max_length=8, null=True, blank=True,
    )

    def create(self):
        client = get_mangopay_api_client()
        mangopay_bank_account = BankAccount()
        mangopay_bank_account.UserId = self.mangopay_user.mangopay_id

        mangopay_bank_account.OwnerName = \
            self.mangopay_user.user.get_full_name()

        mangopay_bank_account.OwnerAddress = unicode(self.address)

        if self.account_type == BA_BIC_IBAN:
            # BIC / IBAN type requires setting IBAN and BIC codes only
            mangopay_bank_account.Details = BankAccountDetailsIBAN()
            mangopay_bank_account.Details.Type = "IBAN"
            mangopay_bank_account.Details.IBAN = self.iban

        elif self.account_type == BA_US:
            mangopay_bank_account.Details = BankAccountDetailsUS()
            mangopay_bank_account.Details.Type = "US"
            mangopay_bank_account.Details.ABA = self.aba
            mangopay_bank_account.Details.DepositAccountType = \
                self.deposit_account_type
            mangopay_bank_account.Details.AccountNumber = self.account_number

        elif self.account_type == BA_OTHER:
            # OTHER type requires setting Details object with Account number
            # country and BIC code.
            mangopay_bank_account.Details = BankAccountDetailsOTHER()
            mangopay_bank_account.Details.Type = "OTHER"
            mangopay_bank_account.Details.AccountNumber = self.account_number

        else:
            if self.account_type in BA_NOT_IMPLEMENTED:
                raise NotImplementedError(
                    "Bank Account Type ({0}) not implemeneted.".format(
                        self.account_type
                    ))
            else:
                raise Exception(
                    "Bank Account Type ({0}) is not valid.".format(
                        self.account_type
                    ))

        # Shared Details for IBAN and Other
        mangopay_bank_account.Details.BIC = self.bic

        if self.country:
            mangopay_bank_account.Details.Country = self.country.code
        else:
            if self.account_type != BA_BIC_IBAN:
                raise Exception("Country is required for Bank Accounts of "
                                "types other than BIC/IBAN")

        created_bank_account = client.users.CreateBankAccount(
            str(self.mangopay_user.mangopay_id),
            mangopay_bank_account)

        self.mangopay_id = created_bank_account.Id

        self.save()


class MangoPayWallet(models.Model):
    mangopay_id = models.PositiveIntegerField(null=True, blank=True)
    mangopay_user = models.ForeignKey(
        MangoPayUser, related_name="mangopay_wallets")
    currency = models.CharField(max_length=3, default="EUR")

    def create(self, description):
        mangopay_wallet = Wallet()
        mangopay_wallet.Owners = [str(self.mangopay_user.mangopay_id)]
        mangopay_wallet.Description = description
        mangopay_wallet.Currency = self.currency
        client = get_mangopay_api_client()
        created_mangopay_wallet = client.wallets.Create(mangopay_wallet)
        self.mangopay_id = created_mangopay_wallet.Id
        self.save()

    def balance(self):
        wallet = self._get()
        return PythonMoney(wallet.Balance.Amount / 100.0,
                           wallet.Balance.Currency)

    def _get(self):
        client = get_mangopay_api_client()
        return client.wallets.Get(self.mangopay_id)


class MangoPayPayIn(models.Model):
    mangopay_id = models.PositiveIntegerField(null=True, blank=True)
    mangopay_user = models.ForeignKey(MangoPayUser, related_name="mangopay_payins")
    mangopay_wallet = models.ForeignKey(MangoPayWallet, related_name="mangopay_payins")

    execution_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=9, choices=TRANSACTION_STATUS_CHOICES,
                              blank=True, null=True)
    debited_funds = MoneyField(default=0, default_currency="EUR",
                               decimal_places=2, max_digits=12)
    fees = MoneyField(default=0, default_currency="EUR", decimal_places=2,
                      max_digits=12)
    result_code = models.CharField(null=True, blank=True, max_length=6)
    type = models.CharField(null=False, blank=False, choices=MANGOPAY_PAYIN_CHOICES, max_length=10)

    # Pay in by card via web - mangopay_card needs custom validation so it's not null on save
    mangopay_card = models.ForeignKey("MangoPayCard", related_name="mangopay_payins", null=True, blank=True)
    secure_mode_redirect_url = models.URLField(null=True, blank=True)

    # Pay in via bank wire
    wire_reference = models.CharField(null=True, blank=True, max_length=50)
    mangopay_bank_account = jsonfield.JSONField(null=True, blank=True)

    def _get_payment_details(self):
        raise NotImplemented

    def _get_execution_details(self):
        raise NotImplemented

    def create(self, tag=None):
        pay_in = PayIn()
        pay_in.Tag = tag
        pay_in.AuthorId = self.mangopay_user.mangopay_id
        pay_in.CreditedUserId = self.mangopay_user.mangopay_id
        pay_in.CreditedWalletId = self.mangopay_wallet.mangopay_id
        pay_in.DebitedFunds = python_money_to_mangopay_money(
            self.debited_funds)
        pay_in.Fees = python_money_to_mangopay_money(self.fees)
        pay_in.PaymentDetails = self._get_payment_details()
        pay_in.ExecutionDetails = self._get_execution_details()
        client = get_mangopay_api_client()
        created_pay_in = client.payIns.Create(pay_in)
        self.mangopay_id = created_pay_in.Id
        self._update(created_pay_in)

    def get(self):
        pay_in = self._get()
        return self._update(pay_in)

    def _get(self):
        client = get_mangopay_api_client()
        return client.payIns.Get(self.mangopay_id)

    def _update(self, pay_in):
        self.execution_date = get_execution_date_as_datetime(pay_in)
        self.status = pay_in.Status
        self.save()
        return self


class MangoPayPayInByCard(MangoPayPayIn):

    class Meta:
        proxy = True

    def create(self, secure_mode_return_url, tag=None):
        self.secure_mode_return_url = secure_mode_return_url
        super(MangoPayPayInByCard, self).create(tag)

    def _get_payment_details(self):
        payment_details = PayInPaymentDetailsCard()
        payment_details.CardType = "CB_VISA_MASTERCARD"
        return payment_details

    def _get_execution_details(self):
        execution_details = PayInExecutionDetailsDirect()
        execution_details.CardId = self.mangopay_card.mangopay_id
        execution_details.SecureModeReturnURL = self.secure_mode_return_url
        execution_details.SecureMode = "DEFAULT"
        return execution_details

    def _update(self, pay_in):
        self.secure_mode_redirect_url = pay_in.\
            ExecutionDetails.SecureModeRedirectURL
        return super(MangoPayPayInByCard, self)._update(pay_in)

    def save(self, *args, **kwargs):
        self.type = CARD_WEB
        if self.mangopay_card is None:
            raise ValidationError("mangopay_card field is required for MangoPayPayInByCard.")
        return super(MangoPayPayInByCard, self).save(*args, **kwargs)


class MangoPayPayInBankWire(MangoPayPayIn):

    class Meta:
        proxy = True

    def _get_payment_details(self):
        payment_details = PayInPaymentDetailsBankWire()
        payment_details.DeclaredDebitedFunds = python_money_to_mangopay_money(self.debited_funds)
        payment_details.DeclaredFees = python_money_to_mangopay_money(self.fees)

        return payment_details

    def _get_execution_details(self):
        return PayInExecutionDetailsDirect()

    def _update(self, pay_in):
        self.wire_reference = pay_in.PaymentDetails.WireReference
        bank_account = pay_in.PaymentDetails.BankAccount.__dict__
        # BankAccount.__dict__ is not recursive so we manually call it for the
        # Details object - fixes https://opbeat.com/fundedbyme/production/errors/273/
        if bank_account["Details"]:
            bank_account["Details"] = bank_account["Details"].__dict__
            self.mangopay_bank_account = bank_account

        return super(MangoPayPayInBankWire, self)._update(pay_in)

    def save(self, *args, **kwargs):
        self.type = BANK_WIRE
        return super(MangoPayPayInBankWire, self).save(*args, **kwargs)


class MangoPayPayOut(models.Model):
    mangopay_id = models.PositiveIntegerField(null=True, blank=True)
    mangopay_user = models.ForeignKey(MangoPayUser,
                                      related_name="mangopay_payouts")
    mangopay_wallet = models.ForeignKey(MangoPayWallet,
                                        related_name="mangopay_payouts")
    mangopay_bank_account = models.ForeignKey(MangoPayBankAccount,
                                              related_name="mangopay_payouts")
    execution_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=9, choices=TRANSACTION_STATUS_CHOICES,
                              blank=True, null=True)
    debited_funds = MoneyField(default=0, default_currency="EUR",
                               decimal_places=2, max_digits=12)
    fees = MoneyField(default=0, default_currency="EUR", decimal_places=2,
                      max_digits=12)

    def create(self, tag=''):
        pay_out = PayOut()
        pay_out.Tag = tag
        pay_out.AuthorId = self.mangopay_user.mangopay_id
        pay_out.DebitedFunds = python_money_to_mangopay_money(
            self.debited_funds)
        pay_out.Fees = python_money_to_mangopay_money(self.fees)
        pay_out.DebitedWalletId = self.mangopay_wallet.mangopay_id
        details = PayOutPaymentDetailsBankWire()
        details.BankAccountId = self.mangopay_bank_account.mangopay_id
        pay_out.MeanOfPaymentDetails = details
        client = get_mangopay_api_client()
        created_pay_out = client.payOuts.Create(pay_out)
        self.mangopay_id = created_pay_out.Id
        return self._update(created_pay_out)

    def get(self):
        if not self.mangopay_id:
            raise ValueError("PayOut need a mangopay id to be retrieved from MangoPay's API.")
        client = get_mangopay_api_client()
        pay_out = client.payOuts.Get(self.mangopay_id)
        return self._update(pay_out)

    def _update(self, pay_out):
        self.execution_date = get_execution_date_as_datetime(pay_out)
        self.status = pay_out.Status
        self.save()
        return self


class MangoPayCard(models.Model):
    mangopay_id = models.PositiveIntegerField(null=True, blank=True)
    expiration_date = models.CharField(blank=True, null=True, max_length=4)
    alias = models.CharField(blank=True, null=True, max_length=16)
    is_active = models.BooleanField(default=False)
    is_valid = models.NullBooleanField()

    def request_card_info(self):
        if self.mangopay_id:
            client = get_mangopay_api_client()
            card = client.cards.Get(self.mangopay_id)
            self.expiration_date = card.ExpirationDate
            self.alias = card.Alias
            self.is_active = card.Active
            if card.Validity == "UNKNOWN":
                self.is_valid = None
            else:
                self.is_valid = card.Validity == "VALID"


class MangoPayCardRegistration(models.Model):
    mangopay_id = models.PositiveIntegerField(null=True, blank=True)
    mangopay_user = models.ForeignKey(
        MangoPayUser, related_name="mangopay_card_registrations")
    mangopay_card = models.OneToOneField(
        MangoPayCard, null=True, blank=True,
        related_name="mangopay_card_registration")

    def create(self, currency):
        client = get_mangopay_api_client()
        card_registration = CardRegistration()
        card_registration.UserId = str(self.mangopay_user.mangopay_id)
        card_registration.Currency = currency
        card_registration = client.cardRegistrations.Create(card_registration)
        self.mangopay_id = card_registration.Id
        self.save()

    def get_preregistration_data(self):
        client = get_mangopay_api_client()
        card_registration = client.cardRegistrations.Get(self.mangopay_id)
        preregistration_data = {
            "preregistrationData": card_registration.PreregistrationData,
            "accessKey": card_registration.AccessKey,
            "cardRegistrationURL": card_registration.CardRegistrationURL}
        return preregistration_data

    def save_mangopay_card_id(self, mangopay_card_id):
        self.mangopay_card.mangopay_id = mangopay_card_id
        self.mangopay_card.save()

    def save(self, *args, **kwargs):
        if not self.mangopay_card:
            mangopay_card = MangoPayCard()
            mangopay_card.save()
            self.mangopay_card = mangopay_card
        super(MangoPayCardRegistration, self).save(*args, **kwargs)


class MangoPayRefund(models.Model):
    mangopay_id = models.PositiveIntegerField(null=True, blank=True)
    mangopay_user = models.ForeignKey(MangoPayUser,
                                      related_name="mangopay_refunds")
    mangopay_pay_in = models.ForeignKey(MangoPayPayIn,
                                        related_name="mangopay_refunds")
    execution_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=9, choices=TRANSACTION_STATUS_CHOICES,
                              blank=True, null=True)
    result_code = models.CharField(null=True, blank=True, max_length=6)

    def create_simple(self):
        pay_in_id = self.mangopay_pay_in.mangopay_id
        refund = Refund()
        refund.InitialTransactionId = pay_in_id
        refund.AuthorId = self.mangopay_user.mangopay_id
        client = get_mangopay_api_client()
        created_refund = client.payIns.CreateRefund(pay_in_id, refund)
        self.status = created_refund.Status
        self.result_code = created_refund.ResultCode
        self.mangopay_id = created_refund.Id
        self.execution_date = get_execution_date_as_datetime(refund)
        self.save()
        return self.status == "SUCCEEDED"


class MangoPayTransfer(models.Model):
    mangopay_id = models.PositiveIntegerField(null=True, blank=True)
    mangopay_debited_wallet = models.ForeignKey(
        MangoPayWallet, related_name="mangopay_debited_wallets")
    mangopay_credited_wallet = models.ForeignKey(
        MangoPayWallet, related_name="mangopay_credited_wallets")
    debited_funds = MoneyField(default=0, default_currency="EUR",
                               decimal_places=2, max_digits=12)
    execution_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=9, choices=TRANSACTION_STATUS_CHOICES,
                              blank=True, null=True)
    result_code = models.CharField(null=True, blank=True, max_length=6)

    def create(self, fees=None):
        transfer = Transfer()
        transfer.DebitedWalletId = self.mangopay_debited_wallet.mangopay_id
        transfer.CreditedWalletId = self.mangopay_credited_wallet.mangopay_id
        transfer.AuthorId =\
            self.mangopay_debited_wallet.mangopay_user.mangopay_id
        transfer.CreditedUserId =\
            self.mangopay_credited_wallet.mangopay_user.mangopay_id
        transfer.DebitedFunds = python_money_to_mangopay_money(
            self.debited_funds)
        if not fees:
            fees = PythonMoney(0, self.debited_funds.currency)
        transfer.Fees = python_money_to_mangopay_money(fees)
        client = get_mangopay_api_client()
        created_transfer = client.transfers.Create(transfer)
        self._update(created_transfer)

    def get(self):
        client = get_mangopay_api_client()
        transfer = client.transfers.Get(self.mangopay_id)
        self._update(transfer)

    def _update(self, transfer):
        self.status = transfer.Status
        self.result_code = transfer.ResultCode
        self.mangopay_id = transfer.Id
        self.execution_date = get_execution_date_as_datetime(transfer)
        self.save()

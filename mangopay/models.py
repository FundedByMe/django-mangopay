import base64
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from mangopaysdk.entities.usernatural import UserNatural
from mangopaysdk.entities.bankaccount import BankAccount
from mangopaysdk.entities.kycdocument import KycDocument
from mangopaysdk.entities.wallet import Wallet
from mangopaysdk.entities.kycpage import KycPage
from mangopaysdk.entities.payout import PayOut
from mangopaysdk.types.money import Money
from mangopaysdk.types.payoutpaymentdetailsbankwire import (
    PayOutPaymentDetailsBankWire)
from mangopaysdk.entities.cardregistration import CardRegistration
from django_countries.fields import CountryField
from django_iban.fields import IBANField, SWIFTBICField
from money import Money as PythonMoney

from .constants import (INCOME_RANGE_CHOICES, LEGAL_PERSON_TYPE_CHOICES,
                        STATUS_CHOICES, DOCUMENT_TYPE_CHOICES, LEGAL_USER,
                        CREATED, STATUS_CHOICES_DICT, NATURAL_USER,
                        DOCUMENT_TYPE_CHOICES_DICT, USER_TYPE_CHOICES,
                        VALIDATED, IDENTITY_PROOF, ADDRESS_PROOF,
                        REGISTRATION_PROOF, ARTICLES_OF_ASSOCIATION,
                        SHAREHOLDER_DECLARATION, PAYOUT_STATUS_CHOICES)
from .client import get_mangopay_api_client


def python_money_to_mangopay_money(python_money):
    return Money(amount=python_money.amount, curreny=python_money.currency)


class MangoPayUser(models.Model):
    mangopay_id = models.PositiveIntegerField(null=True, blank=True)
    user = models.ForeignKey(User, related_name="mangopay_users")
    type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES,
                            null=True)

    # Light Authenication Field:
    birthday = models.DateField(blank=True, null=True)
    country_of_residence = CountryField()
    nationality = CountryField()

    # Regular Authenication Fields:
    address = models.CharField(blank=True, null=True, max_length=254)


class MangoPayNaturalUser(MangoPayUser):
    # Regular Authenication Fields:
    occupation = models.CharField(blank=True, null=True, max_length=254)
    income_range = models.SmallIntegerField(
        blank=True, null=True, choices=INCOME_RANGE_CHOICES)

    def create(self):
        client = get_mangopay_api_client()
        mangopay_user = self._build()
        created_mangopay_user = client.users.Create(mangopay_user)
        self.mangopay_id = created_mangopay_user.Id
        self.save()

    def update(self):
        client = get_mangopay_api_client()
        return client.users.Update(self._build())

    def _build(self):
        mangopay_user = UserNatural()
        mangopay_user.FirstName = self.user.first_name
        mangopay_user.LastName = self.user.last_name
        mangopay_user.Email = self.user.email
        mangopay_user.Birthday = int(self.birthday.strftime("%s"))
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
        return (self.has_light_authenication()
                and self.address
                and self.occupation
                and self.income_range
                and self.mangopay_documents.filter(
                    type=IDENTITY_PROOF, status=VALIDATED).exists())

    def has_strong_authenication(self):
        return (self.has_regular_authenication()
                and self.mangopay_documents.filter(
                    type=ADDRESS_PROOF, status=VALIDATED).exists())


class MangoPayLegalUser(MangoPayUser):
    # Light Authenication Fields:
    legal_person_type = models.CharField(
        default=None, max_length=1,
        choices=LEGAL_PERSON_TYPE_CHOICES)
    business_name = models.CharField(max_length=254)
    generic_business_email = models.EmailField(max_length=254)
    # first_name, last_name, and email belong to the Legal Representative
    # who is not always the same person as the linked user
    first_name = models.CharField(max_length=99)
    last_name = models.CharField(max_length=99)

    # Regular Authenication Fields:
    headquaters_address = models.CharField(blank=True, max_length=254,
                                           null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)

    def __unicode__(self):
        return self.first_name + " " + self.last_name

    def save(self, *args, **kwargs):
        self.type = LEGAL_USER
        return super(MangoPayLegalUser, self).save(*args, **kwargs)

    def has_light_authenication(self):
        return (self.legal_person_type
                and self.business_name
                and self.generic_business_email
                and self.first_name
                and self.last_name
                and self.country_of_residence
                and self.nationality
                and self.birthday)

    def has_regular_authenication(self):
        return (self.has_light_authenication()
                and self.address
                and self.headquaters_address
                and self.address
                and self.email
                and self.mangopay_documents.filter(
                    type=REGISTRATION_PROOF, status=VALIDATED).exists()
                and self.mangopay_documents.filter(
                    type=ARTICLES_OF_ASSOCIATION, status=VALIDATED).exists()
                and self.mangopay_documents.filter(
                    type=SHAREHOLDER_DECLARATION, status=VALIDATED).exists())

    def has_strong_authenication(self):
        return (self.has_regular_authenication()
                and self.mangopay_bank_accounts.exists())


class MangoPayDocument(models.Model):
    mangopay_id = models.PositiveIntegerField(null=True, blank=True)
    mangopay_user = models.ForeignKey(MangoPayUser,
                                      related_name="mangopay_documents")
    type = models.CharField(max_length=2,
                            choices=DOCUMENT_TYPE_CHOICES)
    status = models.CharField(blank=True, null=True, max_length=1,
                              choices=STATUS_CHOICES)
    file = models.FileField(upload_to='mangopay_documents')
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

    def create_page(self):
        page = KycPage()
        self.file.open(mode='rb')
        bytes = base64.b64encode(self.file.read())
        self.file.close()
        page.File = bytes.decode("utf-8")
        client = get_mangopay_api_client()
        client.users.CreateUserKycPage(page, self.mangopay_user.mangopay_id,
                                       self.mangopay_id)

    def get(self):
        client = get_mangopay_api_client()
        document = client.users.GetUserKycDocument(
            self.mangopay_id, self.mangopay_user.mangopay_id)
        self.refused_reason_message = document.RefusedReasonMessage
        self.status = STATUS_CHOICES_DICT[document.Status]
        self.save()

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
        return str(self.mangopay_id) + " " + self.get_status_display()


class MangoPayBankAccount(models.Model):
    mangopay_user = models.ForeignKey(MangoPayUser,
                                      related_name="mangopay_bank_accounts")
    mangopay_id = models.PositiveIntegerField(null=True, blank=True)
    iban = IBANField()
    bic = SWIFTBICField()
    address = models.CharField(max_length=254)

    def create(self):
        client = get_mangopay_api_client()
        mangopay_bank_account = BankAccount()
        mangopay_bank_account.UserId = self.mangopay_user.mangopay_id
        mangopay_bank_account.OwnerName = \
            self.mangopay_user.user.get_full_name()
        mangopay_bank_account.OwnerAddress = self.address
        mangopay_bank_account.IBAN = self.iban
        mangopay_bank_account.BIC = self.bic
        created_bank_account = client.users.CreateBankAccount(
            str(self.mangopay_user.mangopay_id), mangopay_bank_account)
        self.mangopay_id = created_bank_account.Id
        self.save()


class MangoPayWallet(models.Model):
    mangopay_id = models.PositiveIntegerField(null=True, blank=True)
    mangopay_user = models.ForeignKey(
        MangoPayUser, related_name="mangopay_wallets")

    def create(self, currency, description=""):
        mangopay_wallet = Wallet()
        mangopay_wallet.Owners = [str(self.mangopay_user.mangopay_id)]
        mangopay_wallet.Description = description
        mangopay_wallet.Currency = currency
        client = get_mangopay_api_client()
        created_mangopay_wallet = client.wallets.Create(mangopay_wallet)
        self.mangopay_id = created_mangopay_wallet.Id
        self.save()

    def balance(self):
        wallet = self._get()
        return PythonMoney(wallet.Balance.Amount, wallet.Balance.Currency)

    def _get(self):
        client = get_mangopay_api_client()
        return client.wallets.Get(self.mangopay_id)


class MangoPayPayOut(models.Model):
    mangopay_id = models.PositiveIntegerField(null=True, blank=True)
    mangopay_user = models.ForeignKey(MangoPayUser,
                                      related_name="mangopay_payouts")
    mangopay_wallet = models.ForeignKey(MangoPayWallet,
                                        related_name="mangopay_payouts")
    mangopay_bank_account = models.ForeignKey(MangoPayBankAccount,
                                              related_name="mangopay_payouts")
    execution_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=9, choices=PAYOUT_STATUS_CHOICES,
                              blank=True, null=True)

    def create(self, debited_funds=None, fees=None, tag=''):
        pay_out = PayOut()
        pay_out.Tag = tag
        pay_out.AuthorId = self.mangopay_user.mangopay_id
        if not debited_funds:
            debited_funds = self.mangopay_wallet.balance()
        pay_out.DebitedFunds = python_money_to_mangopay_money(debited_funds)
        if not fees:
            fees = PythonMoney(0, debited_funds.currency)
        pay_out.Fees = python_money_to_mangopay_money(fees)
        pay_out.DebitedWalletId = self.mangopay_wallet.mangopay_id
        pay_out.Type = "BANK_WIRE"
        details = PayOutPaymentDetailsBankWire()
        details.BankAccountId = self.mangopay_bank_account.id
        pay_out.MeanOfPaymentDetails = details
        client = get_mangopay_api_client()
        created_pay_out = client.payOuts.Create(pay_out)
        self.mangopay_id = created_pay_out.Id
        self._update(created_pay_out)

    def get(self):
        client = get_mangopay_api_client()
        pay_out = client.payOuts.Get(self.mangopay_id)
        self._update(pay_out)

    def _update(self, pay_out):
        self.status = pay_out.Status
        self.execution_date = datetime.fromtimestamp(pay_out.ExecutionDate)
        self.save()


class MangoPayCard(models.Model):
    mangopay_id = models.PositiveIntegerField(null=True, blank=True)
    expiration_date = models.CharField(blank=True, null=True, max_length=4)
    alias = models.CharField(blank=True, null=True, max_length=16)
    active = models.BooleanField(default=False)
    valid = models.NullBooleanField()

    def request_card_info(self):
        if self.mangopay_id:
            client = get_mangopay_api_client()
            card = client.cards.Get(self.mangopay_id)
            self.expiration_date = card.ExpirationDate
            self.alias = card.Alias
            self.active = card.Active
            if card.Validity == "UNKNOWN":
                self.valid = None
            else:
                self.valid = card.Validity == "VALID"


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
        card_registration.UserId = str(self.mangopay_user.id)
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

    def request_card(self, card_registration_data):
        client = get_mangopay_api_client()
        card_registration = client.cardRegistrations.Get(self.mangopay_id)
        card_registration.RegistrationData = card_registration_data
        card_registration = client.cardRegistrations.Update(card_registration)
        self.mangopay_card.mangopay_id = card_registration.CardId
        self.mangopay_card.save()

    def save(self, *args, **kwargs):
        if not self.mangopay_card:
            mangopay_card = MangoPayCard()
            mangopay_card.save()
            self.mangopay_card = mangopay_card
        super(MangoPayCardRegistration, self).save(*args, **kwargs)

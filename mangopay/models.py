from django.db import models
from django.contrib.auth.models import User

from mangopaysdk.entities.usernatural import UserNatural
from mangopaysdk.entities.bankaccount import BankAccount
from django_countries.fields import CountryField
from django_iban.fields import IBANField, SWIFTBICField

from mangopaysdk.entities.cardregistration import CardRegistration

from .constants import (INCOME_RANGE_CHOICES, LEGAL_PERSON_TYPE_CHOICES,
                        STATUS_CHOICES, DOCUMENT_TYPE_CHOICES)
from .client import get_mangopay_api_client


class MangoPayUser(models.Model):
    mangopay_id = models.PositiveIntegerField(null=True, blank=True)
    user = models.ForeignKey(User)

    # Light Authenication Field:
    birthday = models.DateField(blank=True, null=True)
    country_of_residence = CountryField()
    nationality = CountryField()

    # Regular Authenication Fields:
    address = models.CharField(blank=True, max_length=254)


class MangoPayNaturalUser(MangoPayUser):
    # Regular Authenication Fields:
    occupation = models.CharField(blank=True, max_length=254)
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
        if self.occupation:
            mangopay_user.Occupation = self.occupation
        if self.income_range:
            mangopay_user.IncomeRange = self.income_range
        if self.address:
            mangopay_user.Address = self.address
        if self.mangopay_id:
            mangopay_user.Id = self.mangopay_id
        return mangopay_user


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
    headquaters_address = models.CharField(blank=True, max_length=254)
    email = models.EmailField(max_length=254, blank=True)


class MangoPayDocument(models.Model):
    mangopay_id = models.PositiveIntegerField(null=True, blank=True)
    mangopay_user = models.ForeignKey(MangoPayUser)
    type = models.CharField(max_length=2,
                            choices=DOCUMENT_TYPE_CHOICES)
    status = models.CharField(blank=True, null=True, max_length=1,
                              choices=STATUS_CHOICES)
    file = models.FileField(upload_to='mangopay_documents')
    refused_reason_message = models.CharField(null=True, blank=True,
                                              max_length=255)


class MangoPayBankAccount(models.Model):
    mangopay_user = models.ForeignKey(MangoPayUser)
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


class MangoPayCardRegistration(models.Model):
    mangopay_id = models.PositiveIntegerField(null=True, blank=True)
    mangopay_user = models.ForeignKey(MangoPayUser)
    mangopay_card_id = models.PositiveIntegerField(null=True, blank=True)

    def create(self, currency='EUR'):
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

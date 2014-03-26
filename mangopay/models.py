from django.db import models
from django.contrib.auth.models import User

from django_countries.fields import CountryField
from django_iban.fields import IBANField, SWIFTBICField

from .constants import (INCOME_RANGE_CHOICES, LEGAL_PERSON_TYPE_CHOICES,
                        STATUS_CHOICES, DOCUMENT_TYPE_CHOICES)


class MangoPayUser(models.Model):
    mangopay_id = models.PositiveIntegerField(null=True, blank=True)

    # Light Authenication Field:
    birthday = models.DateField(blank=True, null=True)
    country_of_residence = CountryField()
    nationality = CountryField()

    # Regular Authenication Fields:
    address = models.CharField(blank=True, max_length=254)


class MangoPayNaturalUser(MangoPayUser):
    # Light Authenication Fields:
    user = models.ForeignKey(User)
    # Regular Authenication Fields:
    occupation = models.CharField(blank=True, max_length=254)
    income_range = models.SmallIntegerField(
        blank=True, null=True, choices=INCOME_RANGE_CHOICES)


class MangoPayLegalUser(MangoPayUser):
    # Light Authenication Fields:
    legal_person_type = models.CharField(
        default=None, max_length=1,
        choices=LEGAL_PERSON_TYPE_CHOICES)
    business_name = models.CharField(max_length=254)
    generic_business_email = models.EmailField(max_length=254)
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

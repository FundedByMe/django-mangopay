import datetime

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

import factory

from ..models import (MangoPayNaturalUser, MangoPayBankAccount,
                      MangoPayCardRegistration, MangoPayDocument)
from ..constants import IDENTITY_PROOF


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: 'user{0}'.format(n))
    first_name = "Sven"
    last_name = "Svensons"
    is_active = True
    is_superuser = False
    is_staff = False
    email = "swede@swedishman.com"
    password = make_password("password")


class MangoPayNaturalUserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MangoPayNaturalUser

    mangopay_id = None
    user = factory.SubFactory(UserFactory)
    birthday = datetime.date(1989, 10, 20)
    country_of_residence = "US"
    nationality = "SE"
    address = ""  # Should be None but needs a migration first
    occupation = ""  # Should be None but needs a migration first
    income_range = None


class LightAuthenticationMangoPayNaturalUserFactory(
        MangoPayNaturalUserFactory):
    pass


class RegularAuthenticationMangoPayNaturalUserFactory(
        MangoPayNaturalUserFactory):

    address = "Somewhere over the rainbow"
    occupation = "Cobbler"
    income_range = 1


class MangoPayBankAccountFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MangoPayBankAccount

    mangopay_user = factory.SubFactory(MangoPayNaturalUserFactory)
    mangopay_id = None
    iban = "SE3550000000054910000003"
    bic = "DABAIE2D"
    address = "Hundred Acre Wood"


class MangoPayCardRegistrationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MangoPayCardRegistration

    mangopay_id = None
    mangopay_user = factory.SubFactory(MangoPayNaturalUserFactory)
    mangopay_card_id = None


class MangoPayDocumentFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MangoPayDocument

    mangopay_id = None
    mangopay_user = factory.SubFactory(MangoPayNaturalUserFactory)
    type = IDENTITY_PROOF
    status = None
    file = None
    refused_reason_message = None

import datetime

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.conf import settings

from money import Money
import factory

from ..models import (MangoPayNaturalUser, MangoPayBankAccount,
                      MangoPayLegalUser, MangoPayWallet,
                      MangoPayCardRegistration, MangoPayCard,
                      MangoPayRefund, MangoPayPayIn, MangoPayPayInAbstract,
                      MangoPayPayInBankWire, MangoPayPage,
                      MangoPayPayOut, MangoPayDocument, MangoPayTransfer)
from ..constants import IDENTITY_PROOF, BUSINESS


user_model_factory = getattr(
    settings,
    "AUTH_USER_MODEL_FACTORY",
    "mangopay.tests.factories.UserFactory")


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: 'username{0}'.format(n))
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
    user = factory.SubFactory(user_model_factory)
    birthday = datetime.date(1989, 10, 20)
    country_of_residence = "US"
    nationality = "SE"
    address = None
    occupation = None
    income_range = None


class LightAuthenticationMangoPayNaturalUserFactory(
        MangoPayNaturalUserFactory):
    pass


class RegularAuthenticationMangoPayNaturalUserFactory(
        MangoPayNaturalUserFactory):

    address = "Somewhere over the rainbow"
    occupation = "Cobbler"
    income_range = 1


class MangoPayLegalUserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MangoPayLegalUser

    type = BUSINESS
    mangopay_id = None
    user = factory.SubFactory(user_model_factory)
    birthday = datetime.date(1989, 10, 20)
    country_of_residence = "US"
    nationality = "SE"
    address = None
    business_name = "FundedByMe AB"
    generic_business_email = "hello@fundedbyme.com"
    first_name = "Arno"
    last_name = "Smit"
    headquaters_address = None
    email = None


class LightAuthenticationMangoPayLegalUserFactory(
        MangoPayLegalUserFactory):
    pass


class RegularAuthenticationMangoPayLegalUserFactory(
        MangoPayLegalUserFactory):
    address = "Hammerby Sjostad 3"
    headquaters_address = "Sveavagen 1"
    email = "arno.smit@fundedbyme.com"


class MangoPayBankAccountFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MangoPayBankAccount

    mangopay_user = factory.SubFactory(MangoPayNaturalUserFactory)
    mangopay_id = None
    iban = "SE3550000000054910000003"
    bic = "DABAIE2D"
    address = "Hundred Acre Wood"


class MangoPayCardFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MangoPayCard

    mangopay_id = None
    expiration_date = None
    alias = None
    is_active = False
    is_valid = None


class MangoPayCardRegistrationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MangoPayCardRegistration

    mangopay_id = None
    mangopay_user = factory.SubFactory(MangoPayNaturalUserFactory)
    mangopay_card = factory.SubFactory(MangoPayCardFactory)


class MangoPayDocumentFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MangoPayDocument

    mangopay_id = None
    mangopay_user = factory.SubFactory(MangoPayNaturalUserFactory)
    type = IDENTITY_PROOF
    status = None
    refused_reason_message = None


class MangoPayPageFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MangoPayPage

    document = factory.SubFactory(MangoPayDocumentFactory)
    file = "fake_file.jpg"


class MangoPayWalletFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MangoPayWallet

    mangopay_id = None
    mangopay_user = factory.SubFactory(MangoPayNaturalUserFactory)
    currency = "EUR"


class MangoPayPayOutFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MangoPayPayOut

    mangopay_id = None
    mangopay_user = factory.SubFactory(MangoPayNaturalUserFactory)
    mangopay_wallet = factory.SubFactory(MangoPayWalletFactory)
    mangopay_bank_account = factory.SubFactory(MangoPayBankAccountFactory)
    execution_date = None
    status = None
    debited_funds = Money(0, "EUR")
    fees = Money(0, "EUR")


class MangoPayPayInAbstractFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MangoPayPayInAbstract
    ABSTRACT_FACTORY = True

    mangopay_id = None
    execution_date = None
    status = None
    result_code = None


class MangoPayPayInFactory(MangoPayPayInAbstractFactory):
    FACTORY_FOR = MangoPayPayIn

    mangopay_user = factory.SubFactory(MangoPayNaturalUserFactory)
    mangopay_wallet = factory.SubFactory(MangoPayWalletFactory)
    mangopay_card = factory.SubFactory(MangoPayCardFactory)
    secure_mode_redirect_url = None


class MangoPayPayInBankWireFactory(MangoPayPayInAbstractFactory):
    FACTORY_FOR = MangoPayPayInBankWire

    mangopay_user = factory.SubFactory(MangoPayNaturalUserFactory)
    mangopay_wallet = factory.SubFactory(MangoPayWalletFactory)
    wire_reference = None
    mangopay_bank_account = None


class MangoPayRefundFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MangoPayRefund

    mangopay_id = None
    mangopay_user = factory.SubFactory(MangoPayNaturalUserFactory)
    mangopay_pay_in = factory.SubFactory(MangoPayPayInFactory)
    execution_date = None
    status = None
    result_code = None


class MangoPayTransferFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MangoPayTransfer

    mangopay_id = None
    mangopay_debited_wallet = factory.SubFactory(MangoPayWalletFactory)
    mangopay_credited_wallet = factory.SubFactory(MangoPayWalletFactory)
    debited_funds = Money(0, "EUR")
    execution_date = None
    status = None
    result_code = None

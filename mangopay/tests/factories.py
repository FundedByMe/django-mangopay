from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

import factory

from ..models import MangoPayNaturalUser


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
    country_of_residence = "SE"
    nationality = "US"
    address = None
    occupation = None
    income_range = None

from django.test import TestCase

from mock import patch

from ..models import MangoPayNaturalUser

from .factories import (LightAuthenticationMangoPayNaturalUserFactory,
                        RegularAuthenticationMangoPayNaturalUserFactory)
from .client import MockMangoPayApi


class AbstractMangoPayNaturalUserTests(object):

    @patch("mangopay.models.get_mangopay_api_client")
    def test_user_created(self, mock_client):
        id = 22
        mock_client.return_value = MockMangoPayApi(user_id=id)
        self.assertIsNone(self.user.mangopay_id)
        self.user.create()
        MangoPayNaturalUser.objects.get(id=self.user.id, mangopay_id=id)

    @patch("mangopay.models.get_mangopay_api_client")
    def test_user_updated(self, mock_client):
        mock_client.return_value = MockMangoPayApi(user_id=id)
        self.user.mangopay_id = 33
        self.user.update()


class LightAuthenticationMangoPayNaturalUserTests(
        AbstractMangoPayNaturalUserTests, TestCase):

    def setUp(self):
        self.user = LightAuthenticationMangoPayNaturalUserFactory()


class RegularAuthenticationMangoPayNaturalUserTests(
        AbstractMangoPayNaturalUserTests, TestCase):

    def setUp(self):
        self.user = RegularAuthenticationMangoPayNaturalUserFactory()

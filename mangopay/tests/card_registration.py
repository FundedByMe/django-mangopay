from django.test import TestCase

from mock import patch

from ..models import MangoPayCardRegistration

from .client import MockMangoPayApi
from .factories import MangoPayCardRegistrationFactory


class MangoPayCardRegistrationTests(TestCase):

    def setUp(self):
        self.card_registration = MangoPayCardRegistrationFactory()

    @patch("mangopay.models.get_mangopay_api_client")
    def test_card_registration_created(self, mock_client):
        id = 42
        mock_client.return_value = MockMangoPayApi(card_registration_id=id)
        self.assertIsNone(self.card_registration.mangopay_id)
        self.card_registration.create(currency='EUR')
        self.assertTrue(MangoPayCardRegistration.objects.filter(
            id=self.card_registration.id, mangopay_id=id).exists())

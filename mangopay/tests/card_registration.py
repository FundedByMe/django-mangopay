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

    @patch("mangopay.models.get_mangopay_api_client")
    def test_get_preregistration_data(self, mock_client):
        id = 42
        self.card_registration.mangopay_id = id
        mock_client.return_value = MockMangoPayApi(card_registration_id=id)
        preregistration_data = self.card_registration.get_preregistration_data()
        self.assertIsNotNone(preregistration_data["preregistrationData"])
        self.assertIsNotNone(preregistration_data["accessKey"])
        self.assertIsNotNone(preregistration_data["cardRegistrationURL"])

    def test_save_mangopay_card_id(self):
        card_id = 42
        card_registration_id = 32
        self.card_registration.mangopay_id = card_registration_id
        self.assertIsNone(self.card_registration.mangopay_card.mangopay_id)
        self.card_registration.save_mangopay_card_id(card_id)
        self.assertEqual(self.card_registration.mangopay_card.mangopay_id,
                         card_id)

from django.test import TestCase

from mock import patch

from .client import MockMangoPayApi
from .factories import MangoPayCardFactory


class MangoPayCardTests(TestCase):

    def setUp(self):
        self.card = MangoPayCardFactory()

    @patch("mangopay.models.get_mangopay_api_client")
    def test_request_card_info(self, mock_client):
        id = 42
        mock_client.return_value = MockMangoPayApi(card_id=id)
        self.card.mangopay_id = id
        self.assertIsNone(self.card.alias)
        self.assertIsNone(self.card.expiration_date)
        self.assertIsNone(self.card.is_valid)
        self.assertFalse(self.card.is_active)
        self.card.request_card_info()
        self.assertIsNotNone(self.card.alias)
        self.assertIsNotNone(self.card.expiration_date)
        self.assertTrue(self.card.is_valid)
        self.assertTrue(self.card.is_active)

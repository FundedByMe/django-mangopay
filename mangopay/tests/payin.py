from django.test import TestCase

from mock import patch
from money import Money

from ..models import MangoPayPayIn

from .factories import MangoPayPayInFactory
from .client import MockMangoPayApi


class MangoPayPayInTests(TestCase):

    def setUp(self):
        self.pay_in = MangoPayPayInFactory()

    @patch("mangopay.models.get_mangopay_api_client")
    def test_create(self, mock_client):
        id = 76
        mock_client.return_value = MockMangoPayApi(pay_in_id=id)
        self.assertIsNone(self.pay_in.mangopay_id)
        self.pay_in.create(debited_funds=Money(100, "EUR"),
                           fees=Money(5, "EUR"),
                           secure_mode_return_url="http://test.com")
        MangoPayPayIn.objects.get(id=self.pay_in.id, mangopay_id=id)

    @patch("mangopay.models.get_mangopay_api_client")
    def test_get(self, mock_client):
        mock_client.return_value = MockMangoPayApi()
        self.assertIsNone(self.pay_in.status)
        self.pay_in.get()
        self.pay_in = MangoPayPayIn.objects.get(id=self.pay_in.id)
        self.assertIsNotNone(self.pay_in.status)

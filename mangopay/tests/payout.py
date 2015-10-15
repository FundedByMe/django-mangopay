from django.test import TestCase

from mock import patch
from money import Money

from ..models import MangoPayPayOut

from .factories import MangoPayPayOutFactory
from .client import MockMangoPayApi


class MangoPayPayOutTests(TestCase):

    def setUp(self):
        self.pay_out = MangoPayPayOutFactory(debited_funds=Money(100, "SEK"),
                                             fees=Money(10, "SEK"))

    @patch("mangopay.models.get_mangopay_api_client")
    def test_create_with_defaults(self, mock_client):
        id = 6
        mock_client.return_value = MockMangoPayApi(pay_out_id=id)
        self.assertIsNone(self.pay_out.mangopay_id)
        self.pay_out.create()
        MangoPayPayOut.objects.get(id=self.pay_out.id, mangopay_id=id)

    @patch("mangopay.models.get_mangopay_api_client")
    def test_create(self, mock_client):
        id = 76
        mock_client.return_value = MockMangoPayApi(pay_out_id=id)
        self.assertIsNone(self.pay_out.mangopay_id)
        self.pay_out.create(tag='sdgsd')
        MangoPayPayOut.objects.get(id=self.pay_out.id, mangopay_id=id)

    @patch("mangopay.models.get_mangopay_api_client")
    def test_get(self, mock_client):
        mock_client.return_value = MockMangoPayApi()
        self.pay_out.mangopay_id = 123543
        self.pay_out.save()

        self.assertIsNone(self.pay_out.execution_date)
        self.assertIsNone(self.pay_out.status)

        self.pay_out.get()
        self.pay_out = MangoPayPayOut.objects.get(id=self.pay_out.id)
        self.assertIsNotNone(self.pay_out.execution_date)
        self.assertIsNotNone(self.pay_out.status)

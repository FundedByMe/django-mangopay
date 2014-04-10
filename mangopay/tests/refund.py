from django.test import TestCase

from mock import patch

from ..models import MangoPayRefund

from .factories import MangoPayRefundFactory
from .client import MockMangoPayApi


class MangoPayRefundTests(TestCase):

    def setUp(self):
        self.refund = MangoPayRefundFactory(mangopay_pay_in__mangopay_id=2)

    @patch("mangopay.models.get_mangopay_api_client")
    def test_create(self, mock_client):
        id = 222
        mock_client.return_value = MockMangoPayApi(refund_id=id)
        self.assertIsNone(self.refund.mangopay_id)
        self.refund.create_simple()
        MangoPayRefund.objects.get(id=self.refund.id, mangopay_id=id)

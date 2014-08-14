from django.test import TestCase

from mock import patch

from ..models import MangoPayTransfer

from .factories import MangoPayTransferFactory
from .client import MockMangoPayApi


class MangoPayTransferTests(TestCase):

    def setUp(self):
        self.transfer = MangoPayTransferFactory()

    @patch("mangopay.models.get_mangopay_api_client")
    def test_create(self, mock_client):
        id = 692
        mock_client.return_value = MockMangoPayApi(transfer_id=id)
        self.assertIsNone(self.transfer.mangopay_id)
        self.transfer.create()
        MangoPayTransfer.objects.get(id=self.transfer.id, mangopay_id=id)

    @patch("mangopay.models.get_mangopay_api_client")
    def test_get(self, mock_client):
        mock_client.return_value = MockMangoPayApi()
        self.assertIsNone(self.transfer.status)
        self.transfer.get()
        self.transfer = MangoPayTransfer.objects.get(id=self.transfer.id)
        self.assertIsNotNone(self.transfer.status)

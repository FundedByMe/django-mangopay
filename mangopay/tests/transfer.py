from django.test import TestCase

from money import Money
from mock import patch

from ..models import MangoPayTransfer
from ..tasks import create_mangopay_transfer

from .factories import MangoPayTransferFactory, MangoPayWalletFactory
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


class CreateMangoPayTransferTasksTests(TestCase):

    def setUp(self):
        self.deb_wallet = MangoPayWalletFactory()
        self.cred_wallet = MangoPayWalletFactory()

    @patch("mangopay.models.MangoPayTransfer.create")
    def test_create_mangopay_transfer_calls_transfer_create_method(self, create_mock):
        transfer = MangoPayTransferFactory()
        create_mangopay_transfer.run(transfer_id=transfer.id)
        create_mock.assert_called_once()

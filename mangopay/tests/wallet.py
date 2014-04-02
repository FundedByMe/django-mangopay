from django.test import TestCase

from mock import patch

from ..models import MangoPayWallet

from .factories import MangoPayWalletFactory
from .client import MockMangoPayApi


class MangoPayWalletTests(TestCase):

    def setUp(self):
        self.wallet = MangoPayWalletFactory()

    @patch("mangopay.models.get_mangopay_api_client")
    def test_create_wallet(self, mock_client):
        id = 666
        mock_client.return_value = MockMangoPayApi(wallet_id=id)
        self.assertIsNone(self.wallet.mangopay_id)
        self.wallet.create(currency="EUR", description="Big Spender")
        MangoPayWallet.objects.get(id=self.wallet.id, mangopay_id=id)

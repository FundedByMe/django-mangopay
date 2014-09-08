from django.test import TestCase

from money import Money
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
        self.wallet.create(description="Big Spender")
        MangoPayWallet.objects.get(id=self.wallet.id, mangopay_id=id)

    @patch("mangopay.models.get_mangopay_api_client")
    def test_balance(self, mock_client):
        mock_client.return_value = MockMangoPayApi(wallet_id=id)
        self.assertEqual(self.wallet.balance(), Money(100, "EUR"))

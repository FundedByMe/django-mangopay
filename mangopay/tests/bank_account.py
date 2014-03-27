from django.test import TestCase

from mock import patch

from ..models import MangoPayBankAccount

from .factories import MangoPayBankAccountFactory
from .client import MockMangoPayApi


class MangoPayBankAccountTests(TestCase):

    def setUp(self):
        self.bank_account = MangoPayBankAccountFactory()

    @patch("mangopay.models.get_mangopay_api_client")
    def test_create_bank_account(self, mock_client):
        id = 33322
        mock_client.return_value = MockMangoPayApi(bank_account_id=id)
        self.assertIsNone(self.bank_account.mangopay_id)
        self.bank_account.create()
        MangoPayBankAccount.objects.get(id=self.bank_account.id,
                                        mangopay_id=id)

from django.test import TestCase

from mock import patch

from ..models import MangoPayBankAccount

from .factories import (MangoPayIBANBankAccountFactory,
                        MangoPayOTHERBankAccountFactory)
from .client import MockMangoPayApi

from ..constants import (BA_BIC_IBAN,
                         BA_OTHER)


class MangoPayBankAccountTests(TestCase):

    def setUp(self):
        self.bank_account_iban = MangoPayIBANBankAccountFactory()
        self.bank_account_other = MangoPayOTHERBankAccountFactory()
        self.bank_account_us = MangoPayOTHERBankAccountFactory(account_type="US")

    @patch("mangopay.models.get_mangopay_api_client")
    def test_create_iban_bank_account(self, mock_client):
        id_ = 33322
        mock_client.return_value = MockMangoPayApi(bank_account_id=id_)
        self.assertIsNone(self.bank_account_iban.mangopay_id)
        self.bank_account_iban.create()
        MangoPayBankAccount.objects.get(id=self.bank_account_iban.id,
                                        mangopay_id=id_)
        self.assertEqual(self.bank_account_iban.account_type,
                         BA_BIC_IBAN)
        self.assertTrue(self.bank_account_iban.iban is not "")
        self.assertTrue(self.bank_account_iban.account_number is None)

    @patch("mangopay.models.get_mangopay_api_client")
    def test_create_other_bank_account(self, mock_client):
        id_ = 22333
        mock_client.return_value = MockMangoPayApi(bank_account_id=id_)
        self.assertIsNone(self.bank_account_other.mangopay_id)
        self.bank_account_other.create()
        MangoPayBankAccount.objects.get(id=self.bank_account_other.id,
                                        mangopay_id=id_)
        self.assertEqual(self.bank_account_other.account_type,
                         BA_OTHER)
        self.assertTrue(self.bank_account_other.iban is None)
        self.assertTrue(self.bank_account_other.account_number is not None)

    @patch("mangopay.models.get_mangopay_api_client")
    def test_cannot_create_not_supported_bank_account(self, mock_client):
        id_ = 551412
        mock_client.return_value = MockMangoPayApi(bank_account_id=id_)
        self.assertIsNone(self.bank_account_us.mangopay_id)
        with self.assertRaises(NotImplementedError):
            self.bank_account_us.create()

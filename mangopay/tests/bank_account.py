#coding: utf-8
from django.test import TestCase

from mock import patch

from ..models import MangoPayBankAccount

from .factories import (MangoPayIBANBankAccountFactory,
                        MangoPayUSBankAccountFactory,
                        MangoPayOTHERBankAccountFactory)
from .client import MockMangoPayApi

from ..constants import (BA_BIC_IBAN,
                         BA_US,
                         BA_OTHER)


class MangoPayBankAccountTests(TestCase):

    def setUp(self):
        self.bank_account_iban = MangoPayIBANBankAccountFactory()
        self.bank_account_us = MangoPayUSBankAccountFactory()
        self.bank_account_other = MangoPayOTHERBankAccountFactory()

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

        self.assertIsNone(self.bank_account_iban.account_number)
        self.assertIsNotNone(self.bank_account_iban.iban)

    @patch("mangopay.models.get_mangopay_api_client")
    def test_create_us_bank_account(self, mock_client):
        id_ = 42333
        mock_client.return_value = MockMangoPayApi(bank_account_id=id_)
        self.assertIsNone(self.bank_account_us.mangopay_id)
        self.bank_account_us.create()
        MangoPayBankAccount.objects.get(id=self.bank_account_us.id,
                                        mangopay_id=id_)
        self.assertEqual(self.bank_account_us.account_type,
                         BA_US)

        self.assertIsNone(self.bank_account_us.iban)
        self.assertIsNotNone(self.bank_account_us.aba)
        self.assertIsNotNone(self.bank_account_us.deposit_account_type)
        self.assertIsNotNone(self.bank_account_us.account_number)

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

        self.assertIsNone(self.bank_account_other.iban)
        self.assertIsNotNone(self.bank_account_other.account_number)

    @patch("mangopay.models.get_mangopay_api_client")
    def test_create_with_unicode_characters(self, mock_client):
        id_ = 33322
        mock_client.return_value = MockMangoPayApi(bank_account_id=id_)
        self.assertIsNone(self.bank_account_iban.mangopay_id)
        self.bank_account_iban.address = u"Sveavägen 41"
        self.bank_account_iban.save()

        self.bank_account_iban.create()
        MangoPayBankAccount.objects.get(id=self.bank_account_iban.id,
                                        mangopay_id=id_)
        self.assertEqual(self.bank_account_iban.account_type,
                         BA_BIC_IBAN)

        self.assertIsNone(self.bank_account_iban.account_number)
        self.assertIsNotNone(self.bank_account_iban.iban)

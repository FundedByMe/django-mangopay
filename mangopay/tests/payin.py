from django.test import TestCase
from django.core.exceptions import ValidationError

from mock import patch

from ..models import MangoPayPayInByCard, MangoPayPayInBankWire

from .factories import MangoPayPayInFactory, MangoPayPayInBankWireFactory
from .client import MockMangoPayApi
from mangopay.constants import CARD_WEB, BANK_WIRE


class MangoPayPayByCardInTests(TestCase):

    def setUp(self):
        self.pay_in = MangoPayPayInFactory()
        self.pay_in.__class__ = MangoPayPayInByCard

    @patch("mangopay.models.get_mangopay_api_client")
    def test_create(self, mock_client):
        id = 76
        mock_client.return_value = MockMangoPayApi(pay_in_id=id)
        self.assertIsNone(self.pay_in.mangopay_id)
        self.pay_in.create(secure_mode_return_url="http://test.com")
        MangoPayPayInByCard.objects.get(id=self.pay_in.id, mangopay_id=id)

    @patch("mangopay.models.get_mangopay_api_client")
    def test_get(self, mock_client):
        mock_client.return_value = MockMangoPayApi()
        self.assertIsNone(self.pay_in.secure_mode_redirect_url)
        self.assertIsNone(self.pay_in.status)
        self.pay_in = self.pay_in.get()
        self.assertIsNotNone(self.pay_in.status)
        self.assertIsNotNone(self.pay_in.secure_mode_redirect_url)

    def test_save_sets_type(self):
        payin = MangoPayPayInByCard(mangopay_user=self.pay_in.mangopay_user, mangopay_wallet=self.pay_in.mangopay_wallet, mangopay_card=self.pay_in.mangopay_card)
        payin.save()
        self.assertEqual(CARD_WEB, payin.type)

    def test_save_validates_mangopay_card_is_present(self):
        payin = MangoPayPayInByCard(mangopay_user=self.pay_in.mangopay_user, mangopay_wallet=self.pay_in.mangopay_wallet)
        with self.assertRaises(ValidationError):
            payin.save()


class MangoPayPayInBankWireTests(TestCase):

    def setUp(self):
        self.pay_in = MangoPayPayInBankWireFactory()
        self.pay_in.__class__ = MangoPayPayInBankWire

    @patch("mangopay.models.get_mangopay_api_client")
    def test_create(self, mock_client):
        id = 42
        mock_client.return_value = MockMangoPayApi(pay_in_id=id)
        self.assertIsNone(self.pay_in.mangopay_id)
        self.assertIsNone(self.pay_in.mangopay_bank_account)
        self.assertIsNone(self.pay_in.wire_reference)
        self.pay_in.create()
        MangoPayPayInBankWire.objects.get(id=self.pay_in.id, mangopay_id=id)
        self.assertIsNotNone(self.pay_in.mangopay_bank_account['IBAN'])
        self.assertIsNotNone(self.pay_in.mangopay_bank_account['BIC'])
        self.assertIsNotNone(self.pay_in.wire_reference)

    def test_save_sets_type(self):
        payin = MangoPayPayInBankWire(mangopay_user=self.pay_in.mangopay_user, mangopay_wallet=self.pay_in.mangopay_wallet)
        payin.save()
        self.assertEqual(BANK_WIRE, payin.type)

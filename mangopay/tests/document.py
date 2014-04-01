from django.test import TestCase

from mock import patch

from ..models import MangoPayDocument

from .factories import MangoPayDocumentFactory
from .client import MockMangoPayApi


class MangoPayDocumentTests(TestCase):

    def setUp(self):
        self.document = MangoPayDocumentFactory()

    @patch("mangopay.models.get_mangopay_api_client")
    def test_create_bank_account(self, mock_client):
        id = 3321
        mock_client.return_value = MockMangoPayApi(document_id=id)
        self.assertIsNone(self.document.mangopay_id)
        self.document.create()
        MangoPayDocument.objects.get(id=self.document.id,
                                     mangopay_id=id)

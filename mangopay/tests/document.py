from django.test import TestCase

from mock import patch

from ..models import MangoPayDocument
from ..constants import VALIDATED, VALIDATION_ASKED, CREATED

from .factories import MangoPayDocumentFactory
from .client import MockMangoPayApi


class MangoPayDocumentTests(TestCase):

    def setUp(self):
        self.document = MangoPayDocumentFactory()

    @patch("mangopay.models.get_mangopay_api_client")
    def test_create_document(self, mock_client):
        id = 3321
        mock_client.return_value = MockMangoPayApi(document_id=id)
        self.assertIsNone(self.document.mangopay_id)
        self.document.create()
        MangoPayDocument.objects.get(id=self.document.id,
                                     mangopay_id=id)

    @patch("mangopay.models.get_mangopay_api_client")
    def test_get_document(self, mock_client):
        mock_client.return_value = MockMangoPayApi()
        self.document.get()
        MangoPayDocument.objects.get(id=self.document.id,
                                     status=VALIDATED)

    @patch("mangopay.models.get_mangopay_api_client")
    def test_ask_for_validation_document(self, mock_client):
        mock_client.return_value = MockMangoPayApi()
        self.document.status = CREATED
        self.document.ask_for_validation()
        MangoPayDocument.objects.get(id=self.document.id,
                                     status=VALIDATION_ASKED)

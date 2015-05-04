import os

from django.test import TestCase

from mock import patch

from .factories import MangoPayPageFactory
from .client import MockMangoPayApi


class MangoPayPageTests(TestCase):

    def setUp(self):
        self.page = MangoPayPageFactory()

    @patch("mangopay.models.get_mangopay_api_client")
    def test_create(self, mock_client):
        mock_client.return_value = MockMangoPayApi()
        self.page.file = 'file:///{}/{}'.format(os.getcwd(), "mangopay/tests/test.png")
        self.page.create()

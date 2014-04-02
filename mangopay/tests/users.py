from django.test import TestCase

from mock import patch

from ..models import MangoPayNaturalUser
from ..constants import VALIDATED, IDENTITY_PROOF, NATURAL_USER, LEGAL_USER

from .factories import (LightAuthenticationMangoPayNaturalUserFactory,
                        RegularAuthenticationMangoPayNaturalUserFactory,
                        LightAuthenticationMangoPayLegalUserFactory,
                        RegularAuthenticationMangoPayLegalUserFactory,
                        MangoPayDocumentFactory)
from .client import MockMangoPayApi


class AbstractMangoPayNaturalUserTests(object):

    @patch("mangopay.models.get_mangopay_api_client")
    def test_user_created(self, mock_client):
        id = 22
        mock_client.return_value = MockMangoPayApi(user_id=id)
        self.assertIsNone(self.user.mangopay_id)
        self.user.create()
        MangoPayNaturalUser.objects.get(id=self.user.id, mangopay_id=id)

    @patch("mangopay.models.get_mangopay_api_client")
    def test_user_updated(self, mock_client):
        mock_client.return_value = MockMangoPayApi(user_id=id)
        self.user.mangopay_id = 33
        self.user.update()

    def test_save_saves_type(self):
        self.assertEqual(self.user.type, NATURAL_USER)


class LightAuthenticationMangoPayNaturalUserTests(
        AbstractMangoPayNaturalUserTests, TestCase):

    def setUp(self):
        self.user = LightAuthenticationMangoPayNaturalUserFactory()

    def test_has_authentication_levels(self):
        self.assertTrue(self.user.has_light_authenication())
        self.assertFalse(self.user.has_regular_authenication())
        self.assertFalse(self.user.has_strong_authenication())


class RegularAuthenticationMangoPayNaturalUserTests(
        AbstractMangoPayNaturalUserTests, TestCase):

    def setUp(self):
        self.user = RegularAuthenticationMangoPayNaturalUserFactory()
        MangoPayDocumentFactory(mangopay_user=self.user,
                                type=IDENTITY_PROOF,
                                status=VALIDATED)

    def test_has_authentication_levels(self):
        self.assertTrue(self.user.has_light_authenication())
        self.assertTrue(self.user.has_regular_authenication())
        self.assertFalse(self.user.has_strong_authenication())


class AbstractMangoPayLegalUserTests(object):

    def test_save_saves_type(self):
        self.assertEqual(self.user.type, LEGAL_USER)


class LightAuthenticationMangoPayLegalUserTests(
        AbstractMangoPayLegalUserTests, TestCase):

    def setUp(self):
        self.user = LightAuthenticationMangoPayLegalUserFactory()

    def test_has_authentication_levels(self):
        self.assertTrue(self.user.has_light_authenication())
        self.assertFalse(self.user.has_regular_authenication())
        self.assertFalse(self.user.has_strong_authenication())


class RegularAuthenticationMangoPayLegalUserTests(
        AbstractMangoPayLegalUserTests, TestCase):

    def setUp(self):
        self.user = RegularAuthenticationMangoPayLegalUserFactory()
        MangoPayDocumentFactory(mangopay_user=self.user,
                                type=IDENTITY_PROOF,
                                status=VALIDATED)

    def test_has_authentication_levels(self):
        self.assertTrue(self.user.has_light_authenication())
        self.assertTrue(self.user.has_regular_authenication())
        self.assertFalse(self.user.has_strong_authenication())

from django.test import TestCase

from mock import patch

from ..models import MangoPayNaturalUser, MangoPayLegalUser
from ..constants import (VALIDATED, IDENTITY_PROOF, NATURAL_USER, LEGAL_USER,
                         ARTICLES_OF_ASSOCIATION, REGISTRATION_PROOF,
                         SHAREHOLDER_DECLARATION)

from .factories import (LightAuthenticationMangoPayNaturalUserFactory,
                        RegularAuthenticationMangoPayNaturalUserFactory,
                        LightAuthenticationMangoPayLegalUserFactory,
                        RegularAuthenticationMangoPayLegalUserFactory,
                        MangoPayDocumentFactory)
from .client import MockMangoPayApi


class AbstractMangoPayUserTests(object):

    @patch("mangopay.models.get_mangopay_api_client")
    def test_user_created(self, mock_client):
        id = 22
        mock_client.return_value = MockMangoPayApi(user_id=id)
        self.assertIsNone(self.user.mangopay_id)
        self.user.create()
        self.klass.objects.get(id=self.user.id, mangopay_id=id)

    @patch("mangopay.models.get_mangopay_api_client")
    def test_user_updated(self, mock_client):
        mock_client.return_value = MockMangoPayApi(user_id=id)
        self.user.mangopay_id = 33
        self.user.update()


class AbstractMangoPayNaturalUserTests(AbstractMangoPayUserTests):

    def setUp(self):
        self.klass = MangoPayNaturalUser

    def test_save_saves_type(self):
        self.assertEqual(self.user.type, NATURAL_USER)
        self.assertFalse(self.user.is_legal())
        self.assertTrue(self.user.is_natural())


class LightAuthenticationMangoPayNaturalUserTests(
        AbstractMangoPayNaturalUserTests, TestCase):

    def setUp(self):
        super(LightAuthenticationMangoPayNaturalUserTests, self).setUp()
        self.user = LightAuthenticationMangoPayNaturalUserFactory()

    def test_has_authentication_levels(self):
        self.assertTrue(self.user.has_light_authenication())
        self.assertFalse(self.user.has_regular_authenication())


class RegularAuthenticationMangoPayNaturalUserTests(
        AbstractMangoPayNaturalUserTests, TestCase):

    def setUp(self):
        super(RegularAuthenticationMangoPayNaturalUserTests, self).setUp()
        self.user = RegularAuthenticationMangoPayNaturalUserFactory()
        MangoPayDocumentFactory(mangopay_user=self.user,
                                type=IDENTITY_PROOF,
                                status=VALIDATED)

    def test_has_authentication_levels(self):
        self.assertTrue(self.user.has_light_authenication())
        self.assertTrue(self.user.has_regular_authenication())


class AbstractMangoPayLegalUserTests(AbstractMangoPayUserTests):

    def setUp(self):
        self.klass = MangoPayLegalUser

    def test_save_saves_type(self):
        self.assertEqual(self.user.type, LEGAL_USER)
        self.assertTrue(self.user.is_legal())
        self.assertFalse(self.user.is_natural())


class LightAuthenticationMangoPayLegalUserTests(
        AbstractMangoPayLegalUserTests, TestCase):

    def setUp(self):
        super(LightAuthenticationMangoPayLegalUserTests, self).setUp()
        self.user = LightAuthenticationMangoPayLegalUserFactory()

    def test_has_authentication_levels(self):
        self.assertTrue(self.user.has_light_authenication())
        self.assertFalse(self.user.has_regular_authenication())


class RegularAuthenticationMangoPayLegalUserTests(
        AbstractMangoPayLegalUserTests, TestCase):

    def setUp(self):
        super(RegularAuthenticationMangoPayLegalUserTests, self).setUp()
        self.user = RegularAuthenticationMangoPayLegalUserFactory()
        MangoPayDocumentFactory(mangopay_user=self.user,
                                type=REGISTRATION_PROOF,
                                status=VALIDATED)
        MangoPayDocumentFactory(mangopay_user=self.user,
                                type=SHAREHOLDER_DECLARATION,
                                status=VALIDATED)
        MangoPayDocumentFactory(mangopay_user=self.user,
                                type=ARTICLES_OF_ASSOCIATION,
                                status=VALIDATED)

    def test_has_authentication_levels(self):
        self.assertTrue(self.user.has_light_authenication())
        self.assertTrue(self.user.has_regular_authenication())

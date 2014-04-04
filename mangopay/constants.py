from django.utils.translation import ugettext_lazy as _

LEGAL_USER = "L"
NATURAL_USER = "N"

USER_TYPE_CHOICES = (
    (LEGAL_USER, _("Legal User")),
    (NATURAL_USER, _("Natural User")),
)


INCOME_RANGE_CHOICES = (
    (1, _("Less than 18K Euros")),
    (2, _("Between 18K and 30K Euros")),
    (3, _("Between 30K and 50K Euros")),
    (4, _("Between 50K and 80K Euros")),
    (5, _("Between 80K and 120K Euros")),
    (6, _("Greater than 120K Euros")),
)

BUSINESS = "B"
ORGANIZATION = "O"

LEGAL_PERSON_TYPE_CHOICES = (
    (BUSINESS, "BUSINESS"),
    (ORGANIZATION, "ORGANIZATION"),
)

IDENTITY_PROOF = "IP"
REGISTRATION_PROOF = "RP"
ARTICLES_OF_ASSOCIATION = "AA"
SHAREHOLDER_DECLARATION = "SD"
ADDRESS_PROOF = "AP"

DOCUMENT_TYPE_CHOICES = (
    (IDENTITY_PROOF, "IDENTITY_PROOF"),
    (REGISTRATION_PROOF, "REGISTRATION_PROOF"),
    (ARTICLES_OF_ASSOCIATION, "ARTICLES_OF_ASSOCIATION"),
    (SHAREHOLDER_DECLARATION, "SHAREHOLDER_DECLARATION"),
    (ADDRESS_PROOF, "ADDRESS_PROOF"),
)

DOCUMENT_TYPE_CHOICES_DICT = dict(DOCUMENT_TYPE_CHOICES)

CREATED = "C"
VALIDATION_ASKED = "A"
VALIDATED = "V"
REFUSED = "R"

STATUS_CHOICES = (
    (CREATED, "CREATED"),
    (VALIDATION_ASKED, "VALIDATION_ASKED"),
    (VALIDATED, "VALIDATED"),
    (REFUSED, "REFUSED"),
)

STATUS_CHOICES_DICT = {v: k for k, v in dict(STATUS_CHOICES).iteritems()}

PAYOUT_STATUS_CHOICES = (
    ("CREATED", _("The request is created but not processed.")),
    ("SUCCEEDED", _("The request has been successfully processed.")),
    ("FAILED", _("The request has failed.")),
)

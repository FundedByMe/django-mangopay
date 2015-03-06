from django.utils.translation import ugettext_lazy as _

NATURAL_USER = "N"
BUSINESS = "B"
ORGANIZATION = "O"

USER_TYPE_CHOICES = (
    (NATURAL_USER, _("Natural User")),
    (BUSINESS, "BUSINESS"),
    (ORGANIZATION, "ORGANIZATION"),
)

USER_TYPE_CHOICES_DICT = dict(USER_TYPE_CHOICES)

INCOME_RANGE_CHOICES = (
    (1, "0 - 1,500"),
    (2, "1,500 - 2,499"),
    (3, "2,500 - 3,999"),
    (4, "4,000 - 7,499"),
    (5, "7,500 - 9,999"),
    (6, "10,000 +"),
)
# Income range choices are given per month in euro

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

PENDING = "CREATED"
SUCCEEDED = "SUCCEEDED"
FAILED = "FAILED"

TRANSACTION_STATUS_CHOICES = (
    (PENDING, _("The request is created but not processed.")),
    (SUCCEEDED, _("The request has been successfully processed.")),
    (FAILED, _("The request has failed.")),
)

ERROR_MESSAGES = (
    ("001999", _("Generic Operation error")),
    ("001001", _("Insufficient wallet balance")),
    ("001002", _("Author is not the wallet owner")),
    ("001011", _("Transaction amount is higher than maximum permitted amount")),
    ("001012", _("Transaction amount is lower than minimum permitted amount")),
    ("001013", _("Invalid transaction amount")),
    ("001401", _("Transaction has already been successfully refunded")),
    ("005403", _("The refund cannot exceed initial transaction amount")),
    ("005404", _("The refunded fees cannot exceed initial fee amount")),
    ("005405", _("Balance of client fee wallet insufficient")),
    ("005407", _("Duplicate operation: you cannot refund the same amount more"
                 " than once for a transaction during the same day.")),
    ("105101", _("Invalid card number")),
    ("105102", _("Invalid cardholder name")),
    ("105103", _("Invalid PIN code")),
    ("105104", _("Invalid PIN format")),
    ("105299", _("Token input Error")),
    ("105202", _("Card number: invalid format")),
    ("105203", _("Expiry date: missing or invalid format")),
    ("105204", _("CSC: missing or invalid format")),
    ("105205", _("Callback URL: Invalid format")),
    ("105206", _("Registration data : Invalid format")),
    ("101001", _("The user does not complete transaction")),
    ("101002", _("The transaction has been cancelled by the user")),
    ("101101", _("Transaction refused by the bank. "
                 "No more funds or limit has been reached")),
    ("101102", _("Transaction refused by the bank. "
                 "Amount limit has been reached")),
    ("101103", _("Transaction refused by the terminal")),
    ("101104", _("Transaction refused by the bank. "
                 "The card spent amount limit has been reached")),
    ("101106", _("The card is inactive.")),
    ("101111", _("Maximum number of attempts reached. "
                 "Too much attempts for the same transaction")),
    ("101112", _("Maximum amount exceeded. This is a card limitation on spent "
                 "amount")),
    ("101113", _("Maximum Uses Exceeded. Maximum attempts with this cards "
                 "reached. You must try again after 24 hours.")),
    ("101115", _("Debit limit exceeded. This is a card limitation on spent "
                 "amount")),
    ("101116", _("Amount limit. TThe contribution transaction has failed")),
    ("101119", _("Debit limit exceeded")),
    ("101199", _("Transaction refused. The transaction has been refused by the "
                 "bank. Contact your bank in order to have more information "
                 "about it.")),
    ("101399", _("Secure mode: 3DSecure authentication is not available")),
    ("001599", _("Token processing error. The token has not been created")),
    ("002999", _("The user is blocked due to KYC limitation.")),
    ("008999", _("Fraud policy error")),
    ("008001", _("Counterfeit Card")),
    ("008002", _("Lost Card. A 'lost card' error is a rule carried by the bank"
                 " which deactivates a card due to too many payments or "
                 "attempts.")),
    ("008004", _("Card bin not authorized")),
    ("008005", _("Security violation")),
    ("008006", _("Fraud suspected by the bank")),
    ("008007", _("Opposition on bank account")),
    ("008500", _("Transaction blocked by Fraud Policy")),
    ("008600", _("Wallet blocked by Fraud policy")),
    ("008700", _("User blocked by Fraud policy")),
    ("009199", _("PSP technical error. You could get this error if your card "
                 " is not supported by the payment service provider, or if the "
                 "amount is higher than the maximum amount per transaction")),
    ("009499", _("Bank technical error")),
    ("009999", _("Technical error")),
    ("09101", _("Username/Password is incorrect")),
    ("09102", _("Account is locked or inactive")),
    ("09104", _("Client certificate is disabled")),
    ("09201", _("You do not have permissions to make this API call")),
    ("02625", _("Invalid card number")),
    ("02626", _("Invalid date format")),
    ("02627", _("Invalid CSC number")),
)

ERROR_MESSAGES_DICT = dict(ERROR_MESSAGES)

from django.utils.translation import ugettext_lazy as _

# Users
NATURAL_USER = "N"
BUSINESS = "B"
ORGANIZATION = "O"

USER_TYPE_CHOICES = (
    (NATURAL_USER, _("Natural User")),
    (BUSINESS, "BUSINESS"),
    (ORGANIZATION, "ORGANIZATION"),
)

USER_TYPE_CHOICES_DICT = dict(USER_TYPE_CHOICES)

# Income range choices are given per month in euro
INCOME_RANGE_CHOICES = (
    (1, "0 - 1,500"),
    (2, "1,500 - 2,499"),
    (3, "2,500 - 3,999"),
    (4, "4,000 - 7,499"),
    (5, "7,500 - 9,999"),
    (6, "10,000 +"),
)

# Document types
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

# Document statuses
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

# Bank account types
BA_BIC_IBAN = "BI"
BA_US = "US"
BA_UK = "UK"  # Not Implemented
BA_CA = "CA"  # Not Implemented
BA_OTHER = "O"
BA_NOT_IMPLEMENTED = (
    BA_UK,
    BA_CA
)

MANGOPAY_BANKACCOUNT_TYPE = (
    (BA_BIC_IBAN, _('BIC & IBAN')),
    (BA_US, _('Local US Format')),
    (BA_OTHER, _('Other')),
)

DEPOSIT_CHECKING = "CHECKING"
DEPOSIT_SAVINGS = "SAVINGS"

BA_US_DEPOSIT_ACCOUNT_TYPES = (
    # Options provided by MangoPay
    (DEPOSIT_CHECKING, _('Checking')),
    (DEPOSIT_SAVINGS, _('Savings'))
)


STATUS_CHOICES_DICT = {v: k for k, v in dict(STATUS_CHOICES).iteritems()}

# Transaction statuses
PENDING = "CREATED"
SUCCEEDED = "SUCCEEDED"
FAILED = "FAILED"

TRANSACTION_STATUS_CHOICES = (
    (PENDING, _("The request is created but not processed.")),
    (SUCCEEDED, _("The request has been successfully processed.")),
    (FAILED, _("The request has failed.")),
)

# Pay in types
CARD_WEB = "card-web"
BANK_WIRE = "bank-wire"

MANGOPAY_PAYIN_CHOICES = (
    (BANK_WIRE, _("Pay in by BankWire")),
    (CARD_WEB, _("Pay in by card via web"))
)

ERROR_MESSAGES = (
    ("001999", _("Generic Operation error")),
    ("001001", _("Insufficient wallet balance")),
    ("001002", _("Author is not the wallet owner")),
    ("001011", _("Transaction amount is higher than maximum permitted amount")),
    ("001012", _("Transaction amount is lower than minimum permitted amount")),
    ("001013", _("Invalid transaction amount")),
    ("001014", _("Credited Funds must be more than 0")),

    ("001030", _("User has not been redirected")),
    ("001031", _("User canceled the payment")),

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
    ("101001", _("The user did not complete the transaction")),
    ("101002", _("The transaction has been cancelled by the user")),
    ("001032", _("User is filling in the payment card details")),
    ("001033", _("User has not been redirected then the payment session has expired")),
    ("001034", _("User has let the payment session expire without paying")),

    ("101101", _("Transaction refused by the bank. "
                 "No more funds or limit has been reached")),
    ("101102", _("Transaction refused by the bank. "
                 "Amount limit has been reached")),
    ("101103", _("Transaction refused by the terminal")),
    ("101104", _("Transaction refused by the bank. "
                 "The card spent amount limit has been reached")),
    ("101105", _("The card has expired")),
    ("101106", _("The card is inactive.")),
    ("101410", _("The card is not active")),
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
    ("101301", _("Secure mode: 3DSecure authentication has failed")),

    ("001599", _("Token processing error. The token has not been created")),
    ("101699", _("CardRegistration should return a valid JSON response")),
    ("002999", _("The user is blocked due to KYC limitation.")),
    ("008999", _("Fraud policy error")),
    ("008001", _("Counterfeit Card")),
    ("008002", _("Lost Card. A 'lost card' error is a rule carried by the bank"
                 " which deactivates a card due to too many payments or "
                 "attempts.")),
    ("008003", _("Stolen Card. A 'lost card' error is a rule carried by the bank"
                 " which deactivates a card due to too many payments or "
                 "attempts.")),
    ("008004", _("Card bin not authorized")),
    ("008005", _("Security violation")),
    ("008006", _("Fraud suspected by the bank")),
    ("008007", _("Opposition on bank account")),
    ("008500", _("Transaction blocked by Fraud Policy")),
    ("008600", _("Wallet blocked by Fraud policy")),
    ("008700", _("User blocked by Fraud policy")),
    ("009103", _("PSP configuration error")),

    ("009199", _("PSP technical error. You could get this error if your card "
                 " is not supported by the payment service provider, or if the "
                 "amount is higher than the maximum amount per transaction")),
    ("009499", _("Bank technical error")),
    ("009999", _("Technical error")),

    ("02101", _("Internal Error. There is an issue on the tokenization server (PSP side)")),
    ("02632", _("Method GET is not allowed")),


    ("09101", _("Username/Password is incorrect")),
    ("09102", _("Account is locked or inactive")),
    ("01902", _("This card is not active")),
    ("02624", _("Card expired")),

    ("09104", _("Client certificate is disabled")),
    ("09201", _("You do not have permissions to make this API call")),

    ("02631", _("Too much time taken from the creation of the CardRegistration object to the submission of the Card Details on the Tokenizer Server")),

    ("02625", _("Invalid card number")),
    ("02626", _("Invalid date format")),
    ("02627", _("Invalid CSC number")),
    ("02628", _("Transaction refused"))
)

ERROR_MESSAGES_DICT = dict(ERROR_MESSAGES)

COUNTRY_CHOICES = (
    ('AF', _(u'Afghanistan')),
    ('AX', _(u'\xc5land Islands')),
    ('AL', _(u'Albania')),
    ('DZ', _(u'Algeria')),
    ('AS', _(u'American Samoa')),
    ('AD', _(u'Andorra')),
    ('AO', _(u'Angola')),
    ('AI', _(u'Anguilla')),
    ('AQ', _(u'Antarctica')),
    ('AG', _(u'Antigua and Barbuda')),
    ('AR', _(u'Argentina')),
    ('AM', _(u'Armenia')),
    ('AW', _(u'Aruba')),
    ('AU', _(u'Australia')),
    ('AT', _(u'Austria')),
    ('AZ', _(u'Azerbaijan')),
    ('BS', _(u'Bahamas')),
    ('BH', _(u'Bahrain')),
    ('BD', _(u'Bangladesh')),
    ('BB', _(u'Barbados')),
    ('BY', _(u'Belarus')),
    ('BE', _(u'Belgium')),
    ('BZ', _(u'Belize')),
    ('BJ', _(u'Benin')),
    ('BM', _(u'Bermuda')),
    ('BT', _(u'Bhutan')),
    ('BO', _(u'Bolivia, Plurinational State of')),
    ('BQ', _(u'Bonaire, Sint Eustatius and Saba')),
    ('BA', _(u'Bosnia and Herzegovina')),
    ('BW', _(u'Botswana')),
    ('BV', _(u'Bouvet Island')),
    ('BR', _(u'Brazil')),
    ('IO', _(u'British Indian Ocean Territory')),
    ('BN', _(u'Brunei Darussalam')),
    ('BG', _(u'Bulgaria')),
    ('BF', _(u'Burkina Faso')),
    ('BI', _(u'Burundi')),
    ('KH', _(u'Cambodia')),
    ('CM', _(u'Cameroon')),
    ('CA', _(u'Canada')),
    ('CV', _(u'Cape Verde')),
    ('KY', _(u'Cayman Islands')),
    ('CF', _(u'Central African Republic')),
    ('TD', _(u'Chad')),
    ('CL', _(u'Chile')),
    ('CN', _(u'China')),
    ('CX', _(u'Christmas Island')),
    ('CC', _(u'Cocos (Keeling) Islands')),
    ('CO', _(u'Colombia')),
    ('KM', _(u'Comoros')),
    ('CG', _(u'Congo')),
    ('CD', _(u'Congo, The Democratic Republic of the')),
    ('CK', _(u'Cook Islands')),
    ('CR', _(u'Costa Rica')),
    ('CI', _(u"C\xf4te D'ivoire")),
    ('HR', _(u'Croatia')),
    ('CU', _(u'Cuba')),
    ('CW', _(u'Cura\xe7ao')),
    ('CY', _(u'Cyprus')),
    ('CZ', _(u'Czech Republic')),
    ('DK', _(u'Denmark')),
    ('DJ', _(u'Djibouti')),
    ('DM', _(u'Dominica')),
    ('DO', _(u'Dominican Republic')),
    ('EC', _(u'Ecuador')),
    ('EG', _(u'Egypt')),
    ('SV', _(u'El Salvador')),
    ('GQ', _(u'Equatorial Guinea')),
    ('ER', _(u'Eritrea')),
    ('EE', _(u'Estonia')),
    ('ET', _(u'Ethiopia')),
    ('FK', _(u'Falkland Islands (Malvinas)')),
    ('FO', _(u'Faroe Islands')),
    ('FJ', _(u'Fiji')),
    ('FI', _(u'Finland')),
    ('FR', _(u'France')),
    ('GF', _(u'French Guiana')),
    ('PF', _(u'French Polynesia')),
    ('TF', _(u'French Southern Territories')),
    ('GA', _(u'Gabon')),
    ('GM', _(u'Gambia')),
    ('GE', _(u'Georgia')),
    ('DE', _(u'Germany')),
    ('GH', _(u'Ghana')),
    ('GI', _(u'Gibraltar')),
    ('GR', _(u'Greece')),
    ('GL', _(u'Greenland')),
    ('GD', _(u'Grenada')),
    ('GP', _(u'Guadeloupe')),
    ('GU', _(u'Guam')),
    ('GT', _(u'Guatemala')),
    ('GG', _(u'Guernsey')),
    ('GN', _(u'Guinea')),
    ('GW', _(u'Guinea-bissau')),
    ('GY', _(u'Guyana')),
    ('HT', _(u'Haiti')),
    ('HM', _(u'Heard Island and McDonald Islands')),
    ('VA', _(u'Holy See (Vatican City State)')),
    ('HN', _(u'Honduras')),
    ('HK', _(u'Hong Kong')),
    ('HU', _(u'Hungary')),
    ('IS', _(u'Iceland')),
    ('IN', _(u'India')),
    ('ID', _(u'Indonesia')),
    ('IR', _(u'Iran, Islamic Republic of')),
    ('IQ', _(u'Iraq')),
    ('IE', _(u'Ireland')),
    ('IM', _(u'Isle of Man')),
    ('IL', _(u'Israel')),
    ('IT', _(u'Italy')),
    ('JM', _(u'Jamaica')),
    ('JP', _(u'Japan')),
    ('JE', _(u'Jersey')),
    ('JO', _(u'Jordan')),
    ('KZ', _(u'Kazakhstan')),
    ('KE', _(u'Kenya')),
    ('KI', _(u'Kiribati')),
    ('KP', _(u"Korea, Democratic People's Republic of")),
    ('KR', _(u'Korea, Republic of')),
    ('KW', _(u'Kuwait')),
    ('KG', _(u'Kyrgyzstan')),
    ('LA', _(u"Lao People's Democratic Republic")),
    ('LV', _(u'Latvia')),
    ('LB', _(u'Lebanon')),
    ('LS', _(u'Lesotho')),
    ('LR', _(u'Liberia')),
    ('LY', _(u'Libya')),
    ('LI', _(u'Liechtenstein')),
    ('LT', _(u'Lithuania')),
    ('LU', _(u'Luxembourg')),
    ('MO', _(u'Macao')),
    ('MK', _(u'Macedonia, The Former Yugoslav Republic of')),
    ('MG', _(u'Madagascar')),
    ('MW', _(u'Malawi')),
    ('MY', _(u'Malaysia')),
    ('MV', _(u'Maldives')),
    ('ML', _(u'Mali')),
    ('MT', _(u'Malta')),
    ('MH', _(u'Marshall Islands')),
    ('MQ', _(u'Martinique')),
    ('MR', _(u'Mauritania')),
    ('MU', _(u'Mauritius')),
    ('YT', _(u'Mayotte')),
    ('MX', _(u'Mexico')),
    ('FM', _(u'Micronesia, Federated States of')),
    ('MD', _(u'Moldova, Republic of')),
    ('MC', _(u'Monaco')),
    ('MN', _(u'Mongolia')),
    ('ME', _(u'Montenegro')),
    ('MS', _(u'Montserrat')),
    ('MA', _(u'Morocco')),
    ('MZ', _(u'Mozambique')),
    ('MM', _(u'Myanmar')),
    ('NA', _(u'Namibia')),
    ('NR', _(u'Nauru')),
    ('NP', _(u'Nepal')),
    ('NL', _(u'Netherlands')),
    ('NC', _(u'New Caledonia')),
    ('NZ', _(u'New Zealand')),
    ('NI', _(u'Nicaragua')),
    ('NE', _(u'Niger')),
    ('NG', _(u'Nigeria')),
    ('NU', _(u'Niue')),
    ('NF', _(u'Norfolk Island')),
    ('MP', _(u'Northern Mariana Islands')),
    ('NO', _(u'Norway')),
    ('OM', _(u'Oman')),
    ('PK', _(u'Pakistan')),
    ('PW', _(u'Palau')),
    ('PS', _(u'Palestinian Territory, Occupied')),
    ('PA', _(u'Panama')),
    ('PG', _(u'Papua New Guinea')),
    ('PY', _(u'Paraguay')),
    ('PE', _(u'Peru')),
    ('PH', _(u'Philippines')),
    ('PN', _(u'Pitcairn')),
    ('PL', _(u'Poland')),
    ('PT', _(u'Portugal')),
    ('PR', _(u'Puerto Rico')),
    ('QA', _(u'Qatar')),
    ('RE', _(u'R\xe9union')),
    ('RO', _(u'Romania')),
    ('RU', _(u'Russian Federation')),
    ('RW', _(u'Rwanda')),
    ('BL', _(u'Saint Barth\xe9lemy')),
    ('SH', _(u'Saint Helena, Ascension and Tristan Da Cunha')),
    ('KN', _(u'Saint Kitts and Nevis')),
    ('LC', _(u'Saint Lucia')),
    ('MF', _(u'Saint Martin (French Part)')),
    ('PM', _(u'Saint Pierre and Miquelon')),
    ('VC', _(u'Saint Vincent and the Grenadines')),
    ('WS', _(u'Samoa')),
    ('SM', _(u'San Marino')),
    ('ST', _(u'Sao Tome and Principe')),
    ('SA', _(u'Saudi Arabia')),
    ('SN', _(u'Senegal')),
    ('RS', _(u'Serbia')),
    ('SC', _(u'Seychelles')),
    ('SL', _(u'Sierra Leone')),
    ('SG', _(u'Singapore')),
    ('SX', _(u'Sint Maarten (Dutch Part)')),
    ('SK', _(u'Slovakia')),
    ('SI', _(u'Slovenia')),
    ('SB', _(u'Solomon Islands')),
    ('SO', _(u'Somalia')),
    ('ZA', _(u'South Africa')),
    ('GS', _(u'South Georgia and the South Sandwich Islands')),
    ('SS', _(u'South Sudan')),
    ('ES', _(u'Spain')),
    ('LK', _(u'Sri Lanka')),
    ('SD', _(u'Sudan')),
    ('SR', _(u'Suriname')),
    ('SJ', _(u'Svalbard and Jan Mayen')),
    ('SZ', _(u'Swaziland')),
    ('SE', _(u'Sweden')),
    ('CH', _(u'Switzerland')),
    ('SY', _(u'Syrian Arab Republic')),
    ('TW', _(u'Taiwan, Province of China')),
    ('TJ', _(u'Tajikistan')),
    ('TZ', _(u'Tanzania, United Republic of')),
    ('TH', _(u'Thailand')),
    ('TL', _(u'Timor-leste')),
    ('TG', _(u'Togo')),
    ('TK', _(u'Tokelau')),
    ('TO', _(u'Tonga')),
    ('TT', _(u'Trinidad and Tobago')),
    ('TN', _(u'Tunisia')),
    ('TR', _(u'Turkey')),
    ('TM', _(u'Turkmenistan')),
    ('TC', _(u'Turks and Caicos Islands')),
    ('TV', _(u'Tuvalu')),
    ('UG', _(u'Uganda')),
    ('UA', _(u'Ukraine')),
    ('AE', _(u'United Arab Emirates')),
    ('GB', _(u'United Kingdom')),
    ('US', _(u'United States')),
    ('UM', _(u'United States Minor Outlying Islands')),
    ('UY', _(u'Uruguay')),
    ('UZ', _(u'Uzbekistan')),
    ('VU', _(u'Vanuatu')),
    ('VE', _(u'Venezuela, Bolivarian Republic of')),
    ('VN', _(u'Viet Nam')),
    ('VG', _(u'Virgin Islands, British')),
    ('VI', _(u'Virgin Islands, U.S.')),
    ('WF', _(u'Wallis and Futuna')),
    ('EH', _(u'Western Sahara')),
    ('YE', _(u'Yemen')),
    ('ZM', _(u'Zambia')),
    ('ZW', _(u'Zimbabwe')),
)


# List of ISO 13616-Compliant IBAN Countries
# Pulled from:
# http://www.swift.com/dsp/resources/documents/IBAN_Registry.pdf
# on July 23, 2015.
# Document Version 59, for August 2015

IBAN_COMPLIANT_COUNTRIES = (
    ('AX', _(u'\xc5land Islands')),
    ('AL', _('Albania')),
    ('AD', _('Andorra')),
    ('AT', _('Austria')),
    ('AZ', _('Republic of Azerbaijan')),
    ('BH', _('Bahrain')),
    ('BE', _('Belgium')),
    ('BA', _('Bosnia and Herzegovina')),
    ('BR', _('Brazil')),
    ('BG', _('Bulgaria')),
    ('CR', _('Costa Rica')),
    ('HR', _('Croatia')),
    ('CY', _('Cyprus')),
    ('CZ', _('Czech Republic')),
    ('DK', _('Denmark')),
    ('DO', _('Dominican Republic')),
    ('EE', _('Estonia')),
    ('FI', _('Finland')),
    ('FR', _('France')),
    ('GE', _('Georgia')),
    ('DE', _('Germany')),
    ('GI', _('Gibraltar')),
    ('GR', _('Greece')),
    ('GT', _('Guatemala')),
    ('HU', _('Hungary')),
    ('IS', _('Iceland')),
    ('IE', _('Ireland')),
    ('IL', _('Israel')),
    ('IT', _('Italy')),
    ('JO', _('Jordan')),
    ('KZ', _('Kazakhstan')),
    ('XK', _('Republic of Kosovo')),
    ('KW', _('Kuwait')),
    ('LV', _('Latvia')),
    ('LB', _('Lebanon')),
    ('LI', _('Principality of Liechtenstein')),
    ('LT', _('Lithuania')),
    ('LU', _('Luxembourg')),
    ('MK', _('Macedonia, Former Yugoslav Republic of')),
    ('MT', _('Malta')),
    ('MR', _('Mauritania')),
    ('MU', _('Mauritius')),
    ('MD', _('Moldova')),
    ('MC', _('Monaco')),
    ('ME', _('Montenegro')),
    ('NL', _('The Netherlands')),
    ('NO', _('Norway')),
    ('PK', _('Pakistan')),
    ('PS', _('Palestine, State of')),
    ('PL', _('Poland')),
    ('PT', _('Portugal')),
    ('RO', _('Romania')),
    ('QA', _('Qatar')),
    ('LC', _('Saint Lucia')),
    ('SM', _('San Marino')),
    ('SA', _('Saudi Arabia')),
    ('RS', _('Serbia')),
    ('SK', _('Slovak Republic')),
    ('SI', _('Slovenia')),
    ('ES', _('Spain')),
    ('SE', _('Sweden')),
    ('CH', _('Switzerland')),
    ('TL', _('Timor-Leste')),
    ('TN', _('Tunisia')),
    ('TR', _('Turkey')),
    ('AE', _('United Arab Emirates')),
    ('GB', _('United Kingdom')),
    ('VG', _('Virgin Islands, British'))
)


IBAN_COMPLIANT_COUNTRY_CODES = [code for (code, name) in IBAN_COMPLIANT_COUNTRIES]

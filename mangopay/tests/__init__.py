from users import (LightAuthenticationMangoPayNaturalUserTests,
                   RegularAuthenticationMangoPayNaturalUserTests,
                   LightAuthenticationMangoPayLegalUserTests,
                   RegularAuthenticationMangoPayLegalUserTests)
from bank_account import MangoPayBankAccountTests
from card_registration import MangoPayCardRegistrationTests
from card import MangoPayCardTests
from document import MangoPayDocumentTests
from wallet import MangoPayWalletTests
from payout import MangoPayPayOutTests
from payin import MangoPayPayByCardInTests, MangoPayPayInBankWireTests
from refund import MangoPayRefundTests
from page import MangoPayPageTests
from transfer import MangoPayTransferTests, CreateMangoPayTransferTasksTests

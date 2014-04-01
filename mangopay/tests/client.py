from mangopaysdk.entities.user import User
from mangopaysdk.entities.bankaccount import BankAccount
from mangopaysdk.entities.kycdocument import KycDocument
from mangopaysdk.entities.kycpage import KycPage
from mangopaysdk.entities.cardregistration import CardRegistration


class MockMangoPayApi():

    def __init__(self, user_id=None, bank_account_id=None,
                 card_registration_id=None, document_id=None):
        self.users = MockUserApi(user_id, bank_account_id, document_id)
        self.cardRegistrations = MockCardRegistrationApi(card_registration_id)


class MockUserApi():

    def __init__(self, user_id, bank_account_id, document_id):
        self.user_id = user_id
        self.bank_account_id = bank_account_id
        self.document_id = document_id

    def Create(self, user):
        if isinstance(user, User):
            user.Id = self.user_id
            return user
        else:
            raise BaseException("User must be a User Entity")

    def CreateBankAccount(self, user_id, bank_account):
        if isinstance(bank_account, BankAccount) and isinstance(user_id, str):
            bank_account.Id = self.bank_account_id
            return bank_account
        else:
            raise BaseException("Arguements are the wrong types")

    def Update(self, user):
        if isinstance(user, User) and user.Id:
            return user
        else:
            raise BaseException("User must be a User Entity with an Id")

    def CreateUserKycDocument(self, document, user_id):
        if isinstance(document, KycDocument):
            document.Id = self.document_id
            document.Status = "CREATED"
            return document
        else:
            raise BaseException("Document must be a KycDocument entity")

    def UpdateUserKycDocument(self, document, user_id, document_id):
        if isinstance(document, KycDocument) and document.Id == document_id:
            document.Status = "VALIDATED"
            return document
        else:
            raise BaseException("Arguements are of the wrong types")

    def CreateUserKycPage(self, page, user_id, document_id):
        if isinstance(page, KycPage):
            pass
        else:
            raise BaseException("Page must be a KycPage")


class MockCardRegistrationApi():

    def __init__(self, card_registration_id):
        self.card_registration_id = card_registration_id

    def Create(self, card_registration):
        if isinstance(card_registration, CardRegistration):
            card_registration.Id = self.card_registration_id
            return card_registration
        else:
            raise BaseException(
                "Card Registration must be a CardRegistration Entity")

from mangopaysdk.entities.user import User
from mangopaysdk.entities.bankaccount import BankAccount


class MockMangoPayApi():

    def __init__(self, user_id=None, bank_account_id=None):
        self.users = MockUserApi(user_id, bank_account_id)


class MockUserApi():

    def __init__(self, user_id, bank_account_id):
        self.user_id = user_id
        self.bank_account_id = bank_account_id

    def Create(self, user):
        if isinstance(user, User):
            user.Id = self.user_id
            return user
        else:
            raise("User must be a User Entity")

    def CreateBankAccount(self, user_id, bank_account):
        if isinstance(bank_account, BankAccount) and isinstance(user_id, str):
            bank_account.Id = self.bank_account_id
            return bank_account
        else:
            raise("Arguements are the wrong types")

    def Update(self, user):
        if isinstance(user, User) and user.Id:
            return user
        else:
            raise("User must be a User Entity with an Id")

# Account class
class Account:
    count_id = 0

    # initializer method
    def __init__(self, username, email, password):
        Account.count_id += 1
        self.__account_id = Account.count_id
        self.__username = username
        self.__email = email
        self.__password = password

    # accessor methods
    def get_account_id(self):
        return self.__account_id

    def get_username(self):
        return self.__username

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    # mutator methods

    def set_account_id(self, account_id):
        self.__account_id = account_id

    def set_username(self, username):
        self.__username = username

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

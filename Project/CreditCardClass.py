class CreditCard:
    count_id = 0

    def __init__(self, cardholder, cardnumber, exp_month, exp_year, verification):
        CreditCard.count_id += 1
        self.__creditcard_id = CreditCard.count_id
        self.__cardholder = cardholder
        self.__cardnumber = cardnumber
        self.__exp_month = exp_month
        self.__exp_year = exp_year
        self.__verification = verification

    def get_creditcard_id(self):
        return self.__creditcard_id

    def get_cardholder(self):
        return self.__cardholder

    def get_cardnumber(self):
        return self.__cardnumber

    def get_exp_month(self):
        return self.__exp_month

    def get_exp_year(self):
        return self.__exp_year

    def get_verification_code(self):
        return self.__verification

    def set_creditcard_id(self, creditcard_id):
        self.__creditcard_id = creditcard_id

    def set_cardholder(self, cardholder):
        self.__cardholder = cardholder

    def set_cardnumber(self, cardnumber):
        self.__cardnumber = cardnumber

    def set_exp_month(self, exp_month):
        self.__exp_month = exp_month

    def set_exp_year(self, exp_year):
        self.__exp_year = exp_year

    def set_verification_code(self, verification):
        self.__verification = verification


    #def input_creditcard_info(self):
        #self.__cardholder = input("Cardholder: ")
        #self.__cardnumber = input("Card Number: ")
        #self.__exp_month = input("Expiration Month in MM: ")
        #self.__exp_year = input("Expiration Year in YYYY: ")
        #self.__verification = input("CVV: ")

        # Validate the card number using a regular expression
        #pattern = re.compile(r"^\d{16}$")
        #if not pattern.match(self.__cardnumber):
            #raise ValueError("Invalid card number. It should be 16 digits.")

        # Validate the expiration date
        #current_date = datetime.datetime.now()

        # MM/YYYY format, if number is over 13 or below 1 for month, error comes out
        #if not (1 <= int(self.__exp_month) <= 12) or not (int(self.__exp_year) >= 2023):
            #raise ValueError("Invalid expiration date. It should be in the format MM/YYYY and not expired.")

        # Expire error, if expired, error comes out
        #if int(self.__exp_month) < current_date.month and int(self.__exp_year) <= current_date.year:
            #raise ValueError("Invalid expiration date. It should be in the format MM/YYYY and not expired.")

        # Validate the CVV
        #if not (100 <= int(self.__verification) <= 999):
            #raise ValueError("Invalid CVV. It should be 3 digits.")

    #def display_creditcard_info(self):
        #print("Cardholder: ", self.get_cardholder())
        #print("Card Number: ", self.get_cardnumber())
        #print("Expiration: ", self.get_exp_month(), "/", self.get_exp_year())
        #print("CVV: ", self.get_verification_code())




#with shelve.open('credit_card_data') as db:
    # Store the credit card information
    #db['cardholder'] = credit_card.get_cardholder()
    #db['cardnumber'] = credit_card.get_cardnumber()
    #db['expiration'] = credit_card.get_exp_month() + '/' + credit_card.get_exp_year()
    #db['verification'] = credit_card.get_verification_code()

# To retrieve the data:
#with shelve.open('credit_card_data') as db:
    #cardholder = db['cardholder']
    #cardnumber = db['cardnumber']
    #expiration = db['expiration']
    #verification = db['verification']



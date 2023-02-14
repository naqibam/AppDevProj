class BookingCustomer:
    count_id = 0

    def __init__(self, name, phone_number, email, date, time):
        BookingCustomer.count_id += 1
        self.__booking_id = BookingCustomer.count_id
        self.__name = name
        self.__phone_number = phone_number
        self.__email = email
        self.__date = date
        self.__time = time

    def get_booking_id(self):
        return self.__booking_id

    def get_name(self):
        return self.__name

    def get_phone_number(self):
        return self.__phone_number

    def get_email(self):
        return self.__email

    def get_date(self):
        return self.__date

    def get_time(self):
        return self.__time


    def set_booking_id(self, booking_id):
        self.__booking_id = booking_id

    def set_name(self, name):
        self.__name = name

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def set_email(self, email):
        self.__email = email

    def set_time(self, time):
        self.__time = time

    def set_date(self, date):
        self.__date = date

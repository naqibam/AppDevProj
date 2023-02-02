# Employee class
class Employee:
    count_id = 0

    # initializer method
    def __init__(self, first_name, last_name, gender, position, NRIC):
        Employee.count_id += 1
        self.__employee_id = Employee.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__gender = gender
        self.__position = position
        self.__NRIC = NRIC

    # accessor methods
    def get_employee_id(self):
        return self.__employee_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_gender(self):
        return self.__gender

    def get_position(self):
        return self.__position

    def get_NRIC(self):
        return self.__NRIC

    # mutator methods
    def set_employee_id(self, employee_id):
        self.__employee_id = employee_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_gender(self, gender):
        self.__gender = gender

    def set_position(self, position):
        self.__position = position

    def set_NRIC(self, NRIC):
        self.__NRIC = NRIC

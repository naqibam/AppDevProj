# Inventory class
class Inventory:
    count_id = 0

    # initializer method
    def __init__(self, name, price, quantity):
        Inventory.count_id += 1
        self.__name = name
        self.__price = price
        self.__quantity = quantity

    # accessor methods
    def get_inventory_id(self):
        return self.__inventory_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_quantity(self):
        return self.__quantity

    # mutator methods
    def set_inventory_id(self, inventory_id):
        self.__inventory_id = inventory_id

    def set_name(self, name):
        self.__name = name

    def set_price(self, price):
        self.__price = price

    def set_quantity(self, quantity):
        self.__quantity = quantity

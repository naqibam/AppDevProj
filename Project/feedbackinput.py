from uuid import uuid4
class Contact:
    def __init__(self, name, email, feedback):
        self.__contact_id = uuid4()
        self.__name = name
        self.__email = email
        self.__feedback = feedback

    def get_contact_id(self):
        return self.__contact_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_feedback(self):
        return self.__feedback

    def set_contact_id(self,contact_id):
        self.__contact_id = contact_id

    def set_name(self,name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_feedback(self, feedback):
        self.__feedback = feedback
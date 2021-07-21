from enums import AccountStatus
import datetime
import constants
import configparser
from address import Address



class User(Address):
    path = "users.ini"
    config_user = configparser.ConfigParser()
    config_user.read(path)
    BOOKS_ISSUED_TO_A_USER = 0


    def __init__(self, zip_code, country, state, city, street, house, apartment, id_number, email, phone, name, surname,
                 status=AccountStatus.ACTIVE.name):
        super().__init__(zip_code, country, state, city, street, house, apartment)
        self.__id_number = id_number
        self.__email = email
        self.__phone = phone
        self.status = status
        self.__date_of_membership = datetime.date.today()
        self.__total_books_checkout = 0
        self.books_issued_to_a_user = 0

        if name.isalpha():
            self.__name = name
        else:
            self.__name = "no name"
            print("Only letters may be used in the name")

        if surname.isalpha():
            self.__surname = surname
        else:
            self.__surname = "no surname"
            print("Only letters may be used in the surname")


    def get_id_number(self):
        return self.__id_number

    def set_id_number(self, id):
        self.__id_number = id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def set_email(self, new_email):
        self.__email = new_email

    def get_phone(self):
        return self.__phone

    def set_phone(self, new_phone):
        self.__phone = new_phone

    def get_total_books_checkout(self):
        return self.__total_books_checkout

    def get_date_of_membership(self):
        return self.__date_of_membership

    def get_status(self):
        return self.status

    def add_user(self):

        """  Create a config file for users """

        config = configparser.ConfigParser()
        config.read(self.path)

        try:
            config.add_section(self.__id_number)
            config.set(self.__id_number, "name", f"{self.__name}")
            config.set(self.__id_number, "surname", f"{self.__surname}")
            config.set(self.__id_number, "email", f"{self.__email}")
            config.set(self.__id_number, "phone", f"{self.__phone}")
            config.set(self.__id_number, "status", f"{self.status}")
            config.set(self.__id_number, "books_issued_to_a_user", f"{self.books_issued_to_a_user}")
            config.set(self.__id_number, "address", f"{self.get_zip_code()}, {self.get_country()}, {self.get_city()}, "
                                                    f"{self.get_house()},{self.get_apartment()}")

        except configparser.DuplicateSectionError as er:
            print("This user already exists")

        with open("users.ini", "w", encoding="utf-8") as config_file:
            config.write(config_file)

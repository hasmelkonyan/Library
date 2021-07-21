from abc import ABC

class Address:
    def __init__(self, zip_code, country, state, city, street, house, apartment):
        self.__zip_code = zip_code
        self.__country = country
        self.__state = state
        self.__city = city
        self.__street = street
        self.__house= house
        self.__apartment = apartment

        """
        setters and getters
        """


    def get_zip_code(self):
        return self.__zip_code

    def set_zip_code(self, new_zeep_code):
        self.__zip_code = new_zeep_code

    def get_country(self):
        return self.__country

    def set_country(self, new_country):
        self.__country = new_country

    def get_state(self):
        return self.__state

    def set_state(self, new_state):
        self.__state = new_state

    def get_city(self):
        return self.__city

    def set_city(self, new_city):
        self.__city = new_city

    def get_street(self):
        return self.__street

    def set_street(self, new_street):
        self.__street = new_street

    def get_house(self):
        return self.__house

    def set_house(self, new_house):
        self.__house = new_house

    def get_apartment(self):
        return self.__apartment

    def set_apartment(self, new_apartment):
        self.__apartment = new_apartment





import configparser
from enums import *


class Book:
    path = "LibBooks.ini"
    config_book = configparser.ConfigParser()
    config_book.read(path)

    def __init__(self, isbn, author, title, pages, count, language, available_count=0, subject=BookFormat.NONE.name,
                 status=BookStatus.AVAILABLE.name):
        self.__isbn = isbn
        self.__author = author
        self.__title = title
        self.__pages = pages
        self.__count = count
        self.__available_count = available_count
        self.__subject = subject
        self.__language = language
        self.__status = status

    def get_status(self):
        return self.__status

    def set_status(self, new_status):
        self.__status = new_status

    def get_author(self):
        return self.__author

    def get_title(self):
        return self.__title

    def get_pages(self):
        return self.__pages

    def add_book(self):
        """  Create a config file for books """

        config = configparser.ConfigParser()
        config.read(self.path)
        try:
            config.add_section(self.__isbn)
            config.set(self.__isbn, "author", f"{self.__author}")
            config.set(self.__isbn, "title", f"{self.__title}")
            config.set(self.__isbn, "pages", f"{self.__pages}")
            config.set(self.__isbn, "copies", f"{self.__count}")
            config.set(self.__isbn, "available_copies", f"{self.__available_count}")
            config.set(self.__isbn, "subject", f"{self.__subject}")
            config.set(self.__isbn, "language", f"{self.__language}")
            config.set(self.__isbn, "status", f"{self.__status}")
        except configparser.DuplicateSectionError as e:
            print("This book already exists")

        with open(self.path, "w", encoding="utf-8") as config_file:
            config.write(config_file)

from constants import *
import configparser
from book import Book
from user import User
from datetime import date, datetime
from enums import AccountStatus, BookStatus


class Library:
    sections_books = Book.config_book.sections()
    Book.config_book.read(Book.path)
    sections_users = User.config_user.sections()
    User.config_user.read(User.path)

    def __init__(self):
        self.__books = configparser.ConfigParser()
        self.__users = configparser.ConfigParser()

    def remove_book(self, isbn):

        """If the book with that isbn is found in books config file, do not delete the book, but change the status """

        if isbn in self.sections_books:
            Book.config_book.set(isbn, "status", f"{BookStatus.NONE.name}")

            with open(Book.path, "w") as file:
                Book.config_book.write(file)
        else:
            print("There is no such book")

    def __search_book_by_section(self, isbn):
        if isbn in self.sections_books:
            title = Book.config_book.get(isbn, "title")
            author = Book.config_book.get(isbn, "author")
            print(f"This book is in our library, it is {title}, author is {author}")
        else:
            print("There is no such book")

    def __search_book_by_title(self, title):
        for each_section in self.sections_books:
            if title == Book.config_book.get(each_section, "title"):
                isbn = each_section
                author = Book.config_book.get(isbn, "author")
                print(f"{title} book is in our library, author is {author}, isbn is {isbn}")

    def __search_book_by_author(self, author):
        for each_section in self.sections_books:
            if author == Book.config_book.get(each_section, "author"):
                isbn = each_section
                title = Book.config_book.get(isbn, "title")
                print(f"title: {title}\nauthor:{author}\nisbn: {isbn}\n")

    def search_book(self, val):
        if val in Book.config_book.sections():
            return Library.__search_book_by_section(self, val)
        elif val not in Book.config_book.sections():
            for each_section in Book.config_book.sections():
                if val == Book.config_book.get(each_section, "author"):
                    return Library.__search_book_by_author(self, val)
                elif val == Book.config_book.get(each_section, "title"):
                    return Library.__search_book_by_title(self, val)
        else:
            print("There is no such book in the library")

    def del_user(self, user_id):

        """If user with that id is found in users config file, do not delete the user, but change the account status """

        if user_id in self.sections_users:
            User.config_user.set(user_id, "status", f"{AccountStatus.CLOSED.name}")

            with open(User.path, "w") as file:
                User.config_user.write(file)
        else:
            print("There is no such book in our library")

    def __check_book(self, isbn):
        if isbn in self.sections_books and \
                int(Book.config_book.get(isbn, "available_copies")) > 0:
            return True
        else:
            return False

    def __check_user(self, user_id):
        if user_id not in self.sections_users and \
                User.config_user.get(user_id, "status") != AccountStatus.ACTIVE.name:
            return False
        elif int(User.config_user.get(user_id, "books_issued_to_a_user")) >= MAX_BOOKS_ISSUED_TO_A_USER:
            print("The user has already checked-out maximum number of books")
            return False
        else:
            return True

    def chek_out_book(self, user_id, isbn):

        """
            In books config file reduces by one available copies, in users config file added by one the number of books
            taken by the user
        """

        if self.__check_book(isbn) and self.__check_user(user_id):
            new_available_copies = int(Book.config_book.get(isbn, "available_copies")) - 1
            new_books_issued_to_a_user = int(User.config_user.get(user_id, "books_issued_to_a_user")) + 1
            Book.config_book.set(isbn, 'available_copies', f"{new_available_copies}")
            User.config_user.set(user_id, "books_issued_to_a_user", f"{new_books_issued_to_a_user}")
            User.config_user.set(user_id, f"{isbn}_book_checked_out_time_start", f"{date.today()}")

            with open(User.path, "w") as file:
                User.config_user.write(file)

            with open(Book.path, "w") as f:
                Book.config_book.write(f)
        else:
            return False

    def return_book(self, user_id, isbn):

        """
         In books config file added by one available copies, in users config file reduces by one the number of books
         taken by the user
        """

        new_available_copies = int(Book.config_book.get(isbn, "available_copies")) + 1
        new_books_issued_to_a_user = int(User.config_user.get(user_id, "books_issued_to_a_user")) - 1
        Book.config_book.set(isbn, 'available_copies', f"{new_available_copies}")
        User.config_user.set(user_id, "books_issued_to_a_user", f"{new_books_issued_to_a_user}")
        User.config_user.set(user_id, f"{isbn}_book_checked_out_time_finish", f"{date.today()}")

        with open(User.path, "w") as file:
            User.config_user.write(file)

        with open(Book.path, "w") as f:
            Book.config_book.write(f)

    def days_overdue_books(self, user_id, isbn):

        """ Returns the number of overdue days """

        overdue_days = 0
        date_format = "%Y-%m-%d"
        book_checked_out_time_start = datetime.strptime(User.config_user.get(user_id,
                                                                             f"{isbn}_book_checked_out_time_start"),
                                                        date_format)
        book_checked_out_time_finish = datetime.strptime(
            User.config_user.get(user_id, f"{isbn}_book_checked_out_time_finish"),
            date_format)
        days = book_checked_out_time_finish - book_checked_out_time_start
        days = days.days
        if days > MAX_LENDING_DAYS:
            overdue_days = days - MAX_LENDING_DAYS
        return overdue_days

    def fee_for_book(self, user_id, isbn):

        """ If the user has had overdue days, the fine is calculated for overdue days and added to the principal fee"""

        fee = RETURNING_ON_TIME_PRICE
        if self.days_overdue_books(user_id, isbn) > 0:
            fee = RETURNING_ON_TIME_PRICE + self.days_overdue_books(id, isbn) * FINE_FOR_EACH_DAY_OF_DELAY
        return f"{fee}$"


if __name__ == '__main__':

    l = Library()
    l.search_book("F. Scott Fitzgerald")
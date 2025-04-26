import os

from dynamic_queue import DynamicQueue
from user import User

PATH = "C:/Users/frase/OneDrive - St. John the Baptist School/A-level/Computing/Paper 1 - Programming/Python Programs/Projects/Library Management System"


class Library:
    def __init__(
        self,
        library_name: str,
        books: dict[str, int] = None,
        users: dict[str, str] = None,
        root_path: str = PATH,
    ):
        self.library_name = library_name
        self.books = books
        self.waitlists: dict[str, DynamicQueue] = {}
        self.users: dict[str, User] = {}
        self.PATH = f"{root_path}/{self.library_name}"
        self.user = None

        if not os.path.isdir(f"{self.PATH}"):
            os.makedirs(f"{self.PATH}/Users")
            os.makedirs(f"{self.PATH}/Books")

        if self.books == None:
            self.load_books_from_file()

        for book in self.books.keys():
            self.waitlists.update(self.create_waitlist(book))
        if users != None:
            for username, password in users.items():
                self.users.update({username: User(username, password)})
        else:
            user_files = os.listdir(f"{self.PATH}/Users")
            for user_file in user_files:
                username = user_file.strip(".txt")
                self.users.update(
                    {
                        username: User(
                            username,
                            root_path=f"{self.PATH}/Users",
                            from_file=True,
                        )
                    }
                )

    def menu(self):
        while True:
            username = input("Enter username:\n> ")
            password = input("Enter password:\n> ")

            if self.check_login(username, password):
                user = self.get_user(username)
                print(f"\nWelcome {user.username}\n")
                break
            else:
                print("\nIncorrect username or pasword\n")

        while True:
            while True:
                try:
                    choice = int(
                        input(
                            "\nSelect an option:\n1 - Borrow book\n2 - Return book\n3 - Show currently borrowed books\n4 - Show borrowing history\n5 - Exit\n> "
                        )
                    )
                    if not 1 <= choice <= 5:
                        raise ValueError
                except ValueError:
                    print("Invalid choice")
                else:
                    break

            if choice == 1:
                book = input("Enter name of book:\n> ")
                return_val = self.borrow_book(book, user)
                if return_val == 0:
                    print(f"{book} borrowed successfully")
                elif return_val == 1:
                    print(f"Book not available, added to waitlist")
                elif return_val == 2:
                    print(f"Borrow limit reached, return another book first")
                elif return_val == 3:
                    print(f"Book name invalid")
            elif choice == 2:
                book = input("Enter name of book:\n> ")
                return_val = self.return_book(book, user)
                if return_val == 0:
                    print("Book returned")
                elif return_val == 1:
                    print("Book not borrowed")
                elif return_val == 2:
                    print("Book name invalid")
            elif choice == 3:
                print(user.borrowed_books)
            elif choice == 4:
                print(user.borrow_history.stack)
            else:
                break

        user.save_to_file()

    def check_login(self, username, password) -> bool:
        try:
            if self.users[username].password == password:
                return True
            else:
                return False
        except KeyError:
            return False

    def get_user(self, username) -> User:
        return self.users[username]

    def borrow_book(self, book_name: str, user: User) -> int:
        """Allows user to borrow book if no waitlist, book is available, and user is not over borrow limit. Returns 0 in this case.

        If book is not available, adds the user to a waitlist and returns 1.

        If user is over borrow limit, returns 2.

        If book name is invalid, returns 3"""
        try:
            if self.books[book_name] == 0:
                self.add_user_to_waitlist(book_name, user)
                return 1
            else:
                if user.borrow_book(book_name):
                    self.books[book_name] -= 1
                    return 0
                else:
                    return 2
        except KeyError:
            return 3

    def return_book(self, book_name: str, user: User) -> bool:
        """Returns a book and gives it to the next person in the waitlist if applicable. Returns 0 in the case.

        If book has not been borrowed by user, return 1

        If book name is invalid, returns 2"""
        try:
            self.books[book_name] += 1
        except KeyError:
            return 2

        if user.return_book(book_name):
            self.decrement_waitlist(book_name)
            return 0
        else:
            return 1

    def waitlist_has_users(self, book_name: str):
        """Returns True if the waitlist for a given book has at least one user"""
        return not self.waitlists[book_name].is_empty()

    def create_waitlist(self, book_name: str) -> dict[str, DynamicQueue]:
        """Returns a dictionary entry waitlist for a given book"""
        return {book_name: DynamicQueue(f"{PATH}_{book_name}")}

    def add_user_to_waitlist(self, book_name: str, user: User):
        """Add user to a waitlist for the given book"""
        self.waitlists[book_name].enqueue(user)

    def decrement_waitlist(self, book_name: str):
        """Gives a returned book to the next user in the waitlist if a waitlist has users"""
        if self.waitlist_has_users(book_name):
            waitlist = self.waitlists[book_name]
            # Removes users from the waitlist until a user successfully borrows a book
            while True:
                waitlist_user = waitlist.dequeue()
                if waitlist_user != None:
                    if self.borrow_book(book_name, waitlist_user):
                        break
                    else:
                        continue
                else:
                    break

    def print_available_books(self):
        """Prints book name, if available & waitlist size if applicable"""

    def save_available_books_to_file(self):
        """Write book names & number available to a file, using :: to separate book name & number"""
        save_string = ""
        for book in self.books.items():
            save_string += f"{"::".join([book[0], str(book[1])])}\n"
        with open(f"{self.PATH}/Books/books.txt", mode="w") as file:
            file.write(save_string)

    def load_books_from_file(self):
        """Load books from file and store them in current books"""
        with open(f"{self.PATH}/Books/books.txt", mode="r") as file:
            lines = file.readlines()
        book_data = [lines[i].strip().split("::") for i in range(len(lines))]
        self.books = {}
        for datum in book_data:
            self.books.update({datum[0]: int(datum[1])})

    def quit_library(self):
        if self.user != None:
            self.user.save_to_file()
        self.save_available_books_to_file()

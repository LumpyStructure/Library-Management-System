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
        """Contains the backend methods for running a library system. Persistent files are saved in a folder called the library's name."""
        self.library_name = library_name
        self.books = books
        self.waitlists: dict[str, DynamicQueue] = {}
        self.users: dict[str, User] = {}
        # Stores the set of users who have had attributes changed to know what needs to be written to file
        self.changed_users: set[User] = set()
        self.PATH = f"{root_path}/{self.library_name}"
        self.user = None

        self.check_dirs()

        # Load books from file if none passed in
        if self.books == None:
            self.load_books()

        # If users passed in, add each one to self.users
        if users != None:
            for username, password in users.items():
                self.users.update(
                    {username: User(f"{self.PATH}/Users", username, password)}
                )
                self.changed_users.add(self.users[username])
        else:
            # If not passed in, load from file

            # Gets all the user files in the user folder
            user_files = os.listdir(f"{self.PATH}/Users")

            for user_file in user_files:
                username = user_file.strip(".txt")
                self.users.update(
                    {
                        username: User(
                            f"{self.PATH}/Users",
                            username,
                            from_file=True,
                        )
                    }
                )

        # Tries to load waitlists from a file, creates new ones if they don't exist
        # TODO: allow passing in of waitlists at instantiation (and be able to handle only some being passed in)
        if not self.load_waitlists():
            for book in self.books.keys():
                self.waitlists.update(self.create_waitlist(book))

    def check_dirs(self):
        """Check that all required folders exist and create them if they don't"""
        # Check that main folder exists
        if not os.path.isdir(self.PATH):
            os.makedirs(self.PATH)

        # Check that subfolders exist
        current_dirs = set(os.listdir(self.PATH))
        dirs_to_add = {"Books", "Users", "Waitlists"} - current_dirs
        for _dir in dirs_to_add:
            os.makedirs(f"{self.PATH}/{_dir}")

    def menu(self):
        """Provides a CLI for a user to interact with the library"""

        # Check login details
        while True:
            username = input("Enter username:\n> ")
            password = input("Enter password:\n> ")

            if self.check_login(username, password):
                self.user = self.get_user(username)
                print(f"\nWelcome {self.user.username}\n")
                break
            else:
                print("\nIncorrect username or pasword\n")

        # Main loop
        while True:
            # Get user choice
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
                return_val = self.borrow_book(book, self.user)
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
                return_val = self.return_book(book, self.user)
                if return_val == 0:
                    print("Book returned")
                elif return_val == 1:
                    print("Book not borrowed")
                elif return_val == 2:
                    print("Book name invalid")
            elif choice == 3:
                print(self.user.borrowed_books)
            elif choice == 4:
                print(self.user.borrow_history.stack)
            else:
                break

        self.quit_library()

    def check_login(self, username: str, password: str) -> bool:
        """Checks that a given username and password are valid, returns True if they are"""
        try:
            if self.users[username].password == password:
                return True
            else:
                return False
        except KeyError:
            return False

    def get_user(self, username: str) -> User | None:
        """Returns a user object from a username, or None if username is invalid"""
        try:
            return self.users[username]
        except KeyError:
            return None

    def borrow_book(
        self,
        book_name: str,
        user: User,
        check: bool = False,
        is_from_waitlist: bool = False,
    ) -> int:
        """Allows user to borrow book if no waitlist, book is available, and user is not over borrow limit. Returns 0 in this case.

        If book is not available, adds the user to a waitlist and returns 1.

        If user is over borrow limit, returns 2.

        If book name is invalid, returns 3

        If check is True, no borrowing commands are executed, only state values are returned

        If is_from_waitlist is True, book will be removed from the user's list of waitlists
        """
        try:
            # Checks if there are no books left & adds the user to a waitlist if true
            if self.books[book_name] == 0:
                if not check:
                    self.add_user_to_waitlist(book_name, user)
                return 1
            else:
                # Checks if the user has exceeded their borrow limit
                if user.borrow_book(book_name, check=True):
                    if not check:
                        self.changed_users.add(user)
                        user.borrow_book(book_name)
                        self.books[book_name] -= 1

                    # If the user was on a waitlist, remove the book from the user's list of waitlists
                    if is_from_waitlist and not check:
                        user.waitlists.remove(book_name)
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
            self.changed_users.add(user)
            self.decrement_waitlist(book_name)
            return 0
        else:
            return 1

    def search_books(self, search):
        search_result = []
        for book in self.books.keys():
            if search.casefold() in book.casefold():
                search_result.append(book)

        return search_result

    def waitlist_has_users(self, book_name: str) -> bool:
        """Returns True if the waitlist for a given book has at least one user"""
        return not self.waitlists[book_name].is_empty()

    def create_waitlist(self, book_name: str) -> dict[str, DynamicQueue]:
        """Creates & returns a waitlist for a given book in dictionary form"""
        return {book_name: DynamicQueue(f"{self.PATH}/{book_name}")}

    def add_user_to_waitlist(self, book_name: str, user: User):
        """Add user to a waitlist for the given book"""
        self.waitlists[book_name].enqueue(user)
        user.waitlists.append(book_name)

    def decrement_waitlist(self, book_name: str):
        """Gives a returned book to the next user in the waitlist if a waitlist has users.

        If the next user in the waitlist cannot borrow the book, send them to the back of the waitlist queue
        """
        if self.waitlist_has_users(book_name):
            waitlist = self.waitlists[book_name]
            for _ in range(len(waitlist.queue)):
                waitlist_user = waitlist.dequeue()
                if waitlist_user != None:
                    # Check if the user can borrow the book
                    if self.borrow_book(book_name, waitlist_user, check=True) == 0:
                        self.borrow_book(
                            book_name, waitlist_user, is_from_waitlist=True
                        )
                        break
                    # Send them to the back of the queue if they can't borrow
                    else:
                        self.waitlists[book_name].enqueue(waitlist_user)
                else:
                    break

    def print_available_books(self):
        """Prints book name, if available & waitlist size if applicable. Currently not functional"""

    def save_books(self):
        """Write book names & number available to a file, using :: to separate book name & number"""
        # Create string to write to file
        save_string = ""
        for book in self.books.items():
            save_string += f"{"::".join([book[0], str(book[1])])}\n"

        # Write to file
        with open(f"{self.PATH}/Books/books.txt", mode="w") as file:
            file.write(save_string)

    def load_books(self):
        """Load books from file and store them in current books"""
        # Read from file
        with open(f"{self.PATH}/Books/books.txt", mode="r") as file:
            lines = file.readlines()

        # Split each line into book name & quantity & store it as a 2D list
        book_data = [lines[i].strip().split("::") for i in range(len(lines))]

        # Store book data in self.books
        self.books = {}
        for datum in book_data:
            self.books.update({datum[0]: int(datum[1])})

    def save_waitlists(self):
        """Save waitlists to a file called 'waitlists.txt' with each waitlist on a separate line in the format: <book_name>:::<user1>::<user2>"""
        # Create string to write to file
        save_string = ""
        for waitlist in self.waitlists.items():
            save_string += f"{":::".join([waitlist[0], "::".join([waitlist[1].queue[i].username for i in range(len(waitlist[1].queue))])])}\n"

        # Write to file
        with open(f"{self.PATH}/Waitlists/waitlists.txt", mode="w") as file:
            file.write(save_string)

    def load_waitlists(self) -> bool:
        """Loads waitlists from waitlists.txt, returns True is successful, and False if not"""
        try:
            with open(f"{self.PATH}/Waitlists/waitlists.txt", mode="r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            return False

        self.waitlists = {}
        for line in lines:
            line = line.strip().split(":::")
            waitlist_users = []

            # Extract waitlist users
            for entry in line[1].split("::"):
                if entry != "":
                    waitlist_users.append(self.users[entry])

            self.waitlists.update(
                {line[0]: DynamicQueue(f"{self.PATH}/{line[0]}", waitlist_users)}
            )
        return True

    def quit_library(self):
        """Save current library state to the appropriate files"""
        for user in self.changed_users:
            user.save_to_file()
        self.save_books()
        self.save_waitlists()

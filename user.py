from dynamic_stack import DynamicStack


class User:
    def __init__(
        self,
        username: str,
        root_path: str,
        password: str = None,
        borrow_limit: int = 10,
        from_file: bool = False,
    ):
        self.username = username
        self.USER_FILE = f"{root_path}/{self.username}.txt"
        if from_file:
            self.load_from_file()
        else:
            self.password = password
            self.borrowed_books = []
            self.waitlists = []
            self.borrow_limit = borrow_limit
            self.borrow_history = DynamicStack()

    def borrow_book(self, book_name: str, check: bool = False) -> bool:
        """Adds the given book name to the user's list of borrowed books, if not over their borrow limit.
        Returns True if successful and False if not.

        If check is true, no borrowing commands are executed, only state values are returned.
        """
        if len(self.borrowed_books) < self.borrow_limit:
            if not check:
                self.borrowed_books.append(book_name)
                self.borrow_history.push_stack(book_name)
            return True
        else:
            return False

    def return_book(self, book_name) -> bool:
        """Removes the given book from the user's list of borrowed books. Returns True if successful, and False if not"""
        try:
            self.borrowed_books.remove(book_name)
            return True
        except ValueError:
            return False

    def save_to_file(self):
        """Saves the username, password, borrow limit, current borrowed books and borrow history to a file named user's username"""
        save_string = f"{self.username}\n{self.password}\n{self.borrow_limit}\n{"::".join(self.borrowed_books)}\n{"::".join(self.waitlists)}\n{"::".join(self.borrow_history.stack)}"
        with open(self.USER_FILE, mode="w") as file:
            file.write(save_string)

    def load_from_file(self):
        """Loads details from file named user's username"""
        with open(self.USER_FILE, "r") as file:
            lines = file.readlines()
        self.username = lines[0].strip()
        self.password = lines[1].strip()
        self.borrow_limit = int(lines[2].strip())
        self.borrowed_books = list(lines[3].strip().split("::"))
        self.waitlists = list(lines[4].strip().split("::"))
        self.borrow_history = DynamicStack(list(lines[5].strip().split("::")))

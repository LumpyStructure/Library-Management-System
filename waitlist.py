from dynamic_queue import DynamicQueue
from user import User

PATH = "C:/Users/frase/OneDrive - St. John the Baptist School/A-level/Computing/Paper 1 - Programming/Python Programs/Projects/Library Management System"


class Waitlist:
    def __init__(self, book_name: str, root_path: str = PATH):
        """Creates a waitlist for a given book"""
        self.WAITLIST_PATH = f"{root_path}_{book_name}"
        self.waitlist = DynamicQueue(self.WAITLIST_PATH)

    def waitlist_has_users(self) -> bool:
        """Returns True if the waitlist has users"""
        return self.waitlist.is_empty()

    def add_user_to_waitlist(self, book_name: str, user: User):
        """Add user to a waitlist for the given book.
        Creates a new waitlist if one does not already exist"""

    def decrement_waitlist(self, book_name):
        """Gives a returned book to the next user in the waitlist if a waitlist exists"""

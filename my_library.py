from tkinter import *
from tkinter import ttk

from library import Library
from user import User
from login_screen import LoginScreen
from library_gui import LibraryGUI

my_library = Library("Fleetwood library")
my_library_gui = LibraryGUI(my_library)

my_library_gui.gui()
# my_library.menu()


# # Initial instantiation
# new_library = Library(
#     "Test library",
#     {"Humble Pi": 5, "The Strange Case of Dr Jekyll and Mr Hyde": 1},
#     {"John": "Cats4Life", "Henry": "DogsRule!"},
# )

# new_library = Library("Test library")
# new_library_gui = LibraryGUI(new_library)

# new_library_gui.gui()
# new_library.menu()

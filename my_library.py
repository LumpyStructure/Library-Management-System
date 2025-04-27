from tkinter import *
from tkinter import ttk

from library import Library
from user import User
from login_screen import LoginScreen
from library_gui import LibraryGUI

my_library = Library("Fleetwood library")
# my_library_gui = LibraryGUI(my_library)
new_library = Library(
    "Test library",
    {"Humble Pi": 5, "The Strange Case of Dr Jekyll and Mr Hyde": 1},
    {"John": "Cats4Life", "Henry": "DogsRule!"},
)
# my_library_gui.gui()
# my_library.menu()
new_library.menu()

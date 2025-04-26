from tkinter import *
from tkinter import ttk

from library import Library
from login_screen import LoginScreen


class LibraryGUI:
    def __init__(self, library: Library):
        self.library = library

    def gui(self):
        self.login_screen()

        # Root & Frame
        self.root = Tk()
        self.root.geometry("400x300")
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.create_action_buttons()

        ttk.Separator(self.mainframe, orient=VERTICAL).grid(
            column=2, row=0, rowspan=len(self.action_buttons), sticky=(NS, W)
        )

        self.create_action_results()

        # Add padding to all widgets
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # Hide action results
        for action_result in self.action_results.values():
            for widget in action_result.values():
                widget.grid_remove()

        ttk.Button(self.mainframe, text="Quit", command=self.quit_gui).grid(
            column=3, row=5, sticky=E
        )
        self.root.mainloop()

    def login_screen(self):
        login_screen = LoginScreen(self.library)
        self.library.user = self.library.users[login_screen.username.get()]

    def create_action_buttons(self):
        self.action_buttons = {
            "browse_books": ttk.Button(
                self.mainframe,
                text="Browse books",
                command=self.show_available_books,
            ),
            "borrow_book": ttk.Button(
                self.mainframe,
                text="Borrow book",
                command=self.borrow_book_gui,
            ),
            "return_book": ttk.Button(
                self.mainframe,
                text="Return book",
                command=self.return_book_gui,
            ),
            "borrowed_books": ttk.Button(
                self.mainframe,
                text="Currently borrowed books",
                command=self.show_borrowed_books,
            ),
            "waitlists": ttk.Button(
                self.mainframe,
                text="Waitlists",
                command=self.show_waitlists,
            ),
            "borrow_history": ttk.Button(
                self.mainframe,
                text="Show borrow history",
                command=self.show_borrow_history,
            ),
        }

        for i, button in enumerate(self.action_buttons.values()):
            button.grid(column=1, row=i)

    def create_action_results(self):
        COLUMN = 3
        self.mainframe.grid_columnconfigure(COLUMN, minsize=200)

        # Entry variables
        self.book_to_borrow = StringVar()
        self.book_to_return = StringVar()

        # Action results
        self.action_results = {
            "borrow_book": {
                "label": ttk.Label(self.mainframe, text="Enter book name:"),
                "entry": ttk.Entry(self.mainframe, textvariable=self.book_to_borrow),
                "button": ttk.Button(
                    self.mainframe, text="Borrow", command=self.borrow_book
                ),
            },
            "borrow_book_msgs": {
                "success_msg": ttk.Label(
                    self.mainframe, text="Book borrowed successfully"
                ),
                "waitlist_msg": ttk.Label(
                    self.mainframe, text="Book not available, added to waitlist"
                ),
                "borrow_limit_msg": ttk.Label(
                    self.mainframe, text="Borrow limit reached"
                ),
                "invalid_book_msg": ttk.Label(self.mainframe, text="Invalid book name"),
            },
            "return_book": {
                "label": ttk.Label(self.mainframe, text="Enter book name:"),
                "entry": ttk.Entry(self.mainframe, textvariable=self.book_to_return),
                "button": ttk.Button(
                    self.mainframe, text="Reutrn", command=self.return_book
                ),
            },
            "return_book_msgs": {
                "success_msg": ttk.Label(
                    self.mainframe, text="Book returned successfully"
                ),
                "not_borrowed_msg": ttk.Label(self.mainframe, text="Book not borrowed"),
                "invalid_book_msg": ttk.Label(self.mainframe, text="Invalid book name"),
            },
            "borrowed_books": {
                "label": ttk.Label(
                    self.mainframe,
                    text="Currently borrowed books:",
                ),
                "book_list": ttk.Label(
                    self.mainframe,
                    text="\n".join(self.library.user.borrowed_books),
                ),
            },
            "waitlists": {
                "label": ttk.Label(
                    self.mainframe,
                    text="Waitlists:",
                ),
                "waitlist_list": ttk.Label(
                    self.mainframe,
                    text="\n".join(self.library.user.waitlists),
                ),
            },
            "borrow_history": {
                "label": ttk.Label(
                    self.mainframe,
                    text="Borrowing history:",
                ),
                "book_list": ttk.Label(
                    self.mainframe,
                    text="\n".join(self.library.user.borrow_history.stack),
                ),
            },
        }

        # Adding action results to grid

        # Borrow book
        for i, widget in enumerate(self.action_results["borrow_book"].values()):
            widget.grid(column=COLUMN, row=i)

        for widget in self.action_results["borrow_book_msgs"].values():
            widget.grid(column=COLUMN, row=i + 1)

        # Return book
        for i, widget in enumerate(self.action_results["return_book"].values()):
            widget.grid(column=COLUMN, row=i)

        for widget in self.action_results["return_book_msgs"].values():
            widget.grid(column=COLUMN, row=i + 1)

        # Borrowed books
        for i, widget in enumerate(self.action_results["borrowed_books"].values()):
            widget.grid(column=COLUMN, row=i)

        self.action_results["borrowed_books"]["book_list"].grid_configure(
            rowspan=len(self.action_buttons) - 1
        )

        # Waitlists
        for i, widget in enumerate(self.action_results["waitlists"].values()):
            widget.grid(column=COLUMN, row=i)

        self.action_results["waitlists"]["waitlist_list"].grid_configure(
            rowspan=len(self.action_buttons) - 1
        )

        # Borrow history
        for i, widget in enumerate(self.action_results["borrow_history"].values()):
            widget.grid(column=COLUMN, row=i)

        self.action_results["borrow_history"]["book_list"].grid_configure(
            rowspan=len(self.action_buttons)
        )

    def borrow_book_gui(self):
        self.hide_other_action_results("borrow_book")
        if len(self.action_results["borrow_book"]["label"].grid_info()) == 0:
            for widget in self.action_results["borrow_book"].values():
                widget.grid()
            self.action_results["borrow_book"]["entry"].focus()
        else:
            for widget in self.action_results["borrow_book"].values():
                widget.grid_remove()

    def return_book_gui(self):
        self.hide_other_action_results("return_book")
        if len(self.action_results["return_book"]["label"].grid_info()) == 0:
            for widget in self.action_results["return_book"].values():
                widget.grid()
            self.action_results["return_book"]["entry"].focus()
            self.root.bind("<Return>", self.borrow_book)
        else:
            self.root.unbind("<Return>")
            for widget in self.action_results["return_book"].values():
                widget.grid_remove()

    def show_borrowed_books(self):
        self.hide_other_action_results("borrowed_books")
        if len(self.action_results["borrowed_books"]["label"].grid_info()) == 0:
            self.update_borrowed_books()
            for widget in self.action_results["borrowed_books"].values():
                widget.grid()
        else:
            for widget in self.action_results["borrowed_books"].values():
                widget.grid_remove()

    def update_borrowed_books(self):
        self.action_results["borrowed_books"]["book_list"].configure(
            text="\n".join(self.library.user.borrowed_books)
        )

    def show_borrow_history(self):
        self.hide_other_action_results("borrow_history")
        if len(self.action_results["borrow_history"]["label"].grid_info()) == 0:
            self.update_borrow_history()
            for widget in self.action_results["borrow_history"].values():
                widget.grid()
        else:
            for widget in self.action_results["borrow_history"].values():
                widget.grid_remove()

    def update_borrow_history(self):
        self.action_results["borrow_history"]["book_list"].configure(
            text="\n".join(self.library.user.borrow_history)
        )

    def show_available_books(self):
        pass

    def show_waitlists(self):
        self.hide_other_action_results("waitlists")
        if len(self.action_results["waitlists"]["label"].grid_info()) == 0:
            self.update_waitlists()
            for widget in self.action_results["waitlists"].values():
                widget.grid()
        else:
            for widget in self.action_results["waitlists"].values():
                widget.grid_remove()

    def update_waitlists(self):
        self.action_results["waitlists"]["waitlist_list"].configure(
            text="\n".join(self.library.user.waitlists)
        )

    def hide_other_action_results(self, dont_hide):
        for key, action_result in self.action_results.items():
            if key != dont_hide:
                for widget in action_result.values():
                    widget.grid_remove()

    def hide_all(self, widget_list: list[ttk.Widget]):
        for widget in widget_list:
            widget.grid_remove()

    def borrow_book(self):
        self.hide_all(self.action_results["borrow_book_msgs"].values())
        return_val = self.library.borrow_book(
            self.book_to_borrow.get(), self.library.user
        )
        if return_val == 0:
            self.action_results["borrow_book_msgs"]["success_msg"].grid()
        elif return_val == 1:
            self.action_results["borrow_book_msgs"]["waitlist_msg"].grid()
        elif return_val == 2:
            self.action_results["borrow_book_msgs"]["borrow_limit_msg"].grid()
        else:
            self.action_results["borrow_book_msgs"]["invalid_book_msg"].grid()

    def return_book(self):
        self.hide_all(self.action_results["return_book_msgs"].values())
        return_val = self.library.return_book(
            self.book_to_return.get(), self.library.user
        )
        if return_val == 0:
            self.action_results["return_book_msgs"]["success_msg"].grid()
        elif return_val == 1:
            self.action_results["return_book_msgs"]["not_borrowed_msg"].grid()
        else:
            self.action_results["return_book_msgs"]["invalid_book_msg"].grid()

    def quit_gui(self):
        self.library.quit_library()
        self.root.destroy()

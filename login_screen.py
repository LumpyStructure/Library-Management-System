from tkinter import *
from tkinter import ttk


class LoginScreen:
    def __init__(self, user_system, root: Tk = None):
        self.user_system = user_system
        if root == None:
            self.root = Tk()
        else:
            self.root = root

        self.root.title("Login")

        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.username = StringVar()
        username_entry = ttk.Entry(self.mainframe, width=12, textvariable=self.username)
        username_entry.grid(column=2, row=2, columnspan=2, sticky=(W, E))

        self.password = StringVar()
        ttk.Entry(self.mainframe, width=12, textvariable=self.password).grid(
            column=2, row=3, columnspan=2, sticky=(W, E)
        )

        ttk.Button(self.mainframe, text="Login", command=self.login).grid(
            column=3, row=4, sticky=E
        )

        ttk.Label(self.mainframe, text="Username: ").grid(column=1, row=2, sticky=E)
        ttk.Label(self.mainframe, text="Password: ").grid(column=1, row=3, sticky=E)

        self.error_text = ttk.Label(self.root, text="Incorrect username or password")
        self.error_text.grid(
            column=2, row=1, columnspan=2, sticky=E, in_=self.mainframe
        )
        self.error_text.lower(self.mainframe)

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
        username_entry.focus()
        self.root.bind("<Return>", self.login)
        self.root.mainloop()

    def login(self, *args):
        if self.user_system.check_login(self.username.get(), self.password.get()):
            self.root.destroy()
        else:
            self.error_text.lift(self.mainframe)

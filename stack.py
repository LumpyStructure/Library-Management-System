class Stack:
    def __init__(
        self,
        root_path: str,
        data: list = None,
        length: int = 0,
        show_menu: bool = False,
    ) -> None:

        self.root_path = root_path
        self.stack = []
        self.prev_stack = []
        self.pointer = 0
        self.prev_pointer = 0
        if show_menu:
            self.menu()
        else:
            self.create_stack(length if length != 0 else len(data))
            for datum in data:
                self.push_stack(datum)

    def menu(self) -> None:
        func_list = [
            "item = input('Enter item to add: ')\nif not self.push_stack(item):\n    print('Stack is full')",
            "self.pop_stack()",
            "print(self.peek_stack())",
            "self.view_stack()",
            "self.undo()",
            "if not self.save_stack():\n    print('Stack not full')",
            "if not self.load_stack():\n    print('File does not exist')",
            "if self.is_full():\n    exit()\nelse:\n    print('List not full')",
        ]
        print("\033c")
        load_from_file = (
            True if input("Load stack from file? (Y/N): ").casefold() == "y" else False
        )
        if load_from_file:
            self.load_stack()
        else:
            while True:
                try:
                    length = int(input("Enter length of stack: "))
                except ValueError:
                    print("Invalid input")
                else:
                    break
            self.create_stack(length)

        while True:
            while True:
                try:
                    choice = int(
                        input(
                            "1: Push\n2: Pop\n3: Peek\n4: View stack\n5: Undo\n6: Save to file\n7: Load from file\n8: Finish\n"
                        )
                    )
                    if not 1 <= choice <= 8:
                        raise ValueError
                except ValueError:
                    print("Invalid input")
                else:
                    break

            exec(func_list[choice - 1])

    def create_stack(self, length: int) -> list:
        """Creates an empty stack with a given length"""
        self.stack = [None for _ in range(length)]
        self.prev_stack = self.stack.copy()

    def push_stack(self, item: any) -> bool:
        """Adds item to the stack if not full. Returns True if successful and False if not"""
        self.prev_stack = self.stack.copy()
        self.prev_pointer = self.pointer
        if not self.is_full():
            self.stack[self.pointer] = item
            self.pointer += 1
            return True
        else:
            return False

    def pop_stack(self) -> str | None:
        """Removes the top item from the stack. Returns item that was popped or None"""
        self.prev_stack = self.stack.copy()
        self.prev_pointer = self.pointer
        if not self.is_empty():
            self.pointer -= 1
            self.stack[self.pointer] = None
            return self.prev_stack[self.prev_pointer]
        return None

    def peek_stack(self) -> str:
        """Returns the top item of the stack"""
        return self.stack[self.pointer - 1]

    def view_stack(self) -> None:
        """Prints the whole stack"""
        for i in range(len(self.stack)):
            print(self.stack[len(self.stack) - 1 - i])

    def is_full(self) -> bool:
        """Returns True if the stack is full (has no None types)"""
        if None in self.stack:
            return False
        else:
            return True

    def is_empty(self) -> bool:
        """Returns True if the stack is empty (has all None types)"""
        for i in self.stack:
            if i != None:
                return False
        return True

    def undo(self) -> None:
        """Reverts stack to the state of prev_stack"""
        self.stack = self.prev_stack.copy()
        self.pointer = self.prev_pointer

    def save_stack(self, file_name: str = "") -> bool:
        """Saves stack to a user defined text file"""
        if self.is_full():
            if file_name == "":
                file_name = input("Enter file name: ")

            with open(f"{self.root_path}{file_name}.txt", "w") as file:
                file.write(f"{len(self.stack)}\n")
                for i in self.stack:
                    file.write(f"{i}\n")
            return True
        else:
            return False

    def load_stack(self, file_name: str = "") -> bool:
        """Loads stack from a text file. If no file name given, will get user input"""
        if file_name == "":
            file_name = input("Enter file name: ")

        try:
            with open(f"{self.root_path}{file_name}.txt", "r") as file:
                self.create_stack(int(file.readline().strip()))
                for line in file.readlines():
                    self.push_stack(line.strip())
        except FileNotFoundError:
            return False
        else:
            return True

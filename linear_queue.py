class LinearQueue:

    def __init__(
        self,
        root_path: str = "",
        data: list = [],
        length: str = 0,
        show_menu: bool = False,
    ) -> None:

        self.root_path = root_path
        self.queue = []
        self.prev_queue = []
        self.start_pointer = 0
        self.end_pointer = 0
        self.prev_pointer = 0
        if show_menu:
            self.menu()
        else:
            self.create_queue(length if length != 0 else len(data))
            for datum in data:
                self.enqueue(datum)

    def menu(self) -> None:
        func_list = [
            "item = self.get_usr_item()\nif not self.enqueue(item):\n    print('Queue is full')",
            "if not self.dequeue():\n    print('No items to dequeue')",
            "print(self.peek_queue())",
            "self.view_queue()",
            "self.undo()",
            "if not self.save_queue():\n    print('Queue not full')",
            "if not self.load_queue():\n    print('File does not exist')",
            "if self.is_full():\n    exit()\nelse:\n    print('List not full')",
        ]
        print("\033c")
        load_from_file = (
            True if input("Load queue from file? (Y/N): ").casefold() == "y" else False
        )
        if load_from_file:
            self.load_queue()
        else:
            while True:
                try:
                    length = int(input("Enter length of queue: "))
                except ValueError:
                    print("Invalid input")
                else:
                    break
            self.create_queue(length)

        while True:
            while True:
                try:
                    choice = int(
                        input(
                            "1: Enqueue\n2: Dequeue\n3: Peek\n4: View queue\n5: Undo\n6: Save to file\n7: Load from file\n8: Finish\n"
                        )
                    )
                    if not 1 <= choice <= 8:
                        raise ValueError
                except ValueError:
                    print("Invalid input")
                else:
                    break

            exec(func_list[choice - 1])

    def create_queue(self, length) -> list:
        """Creates an empty queue with a given length"""
        self.queue = [None for _ in range(length)]
        self.prev_queue = self.queue.copy()

    def get_usr_item(self) -> str:
        while True:
            try:
                item = input("Enter item to add: ")
                if item == "None":
                    raise ValueError
            except ValueError:
                print("Item cannot be 'None'")
            else:
                return item

    def enqueue(self, item) -> bool:
        """Adds item to the queue if not full. Returns True if successful and False if not"""
        self.prev_queue = self.queue.copy()
        self.prev_pointer = self.end_pointer
        if not self.is_full():
            self.queue[self.end_pointer] = item
            self.end_pointer += 1
            return True
        else:
            return False

    def dequeue(self) -> bool:
        """Removes the top item from the queue. Returns True if successful and False if not"""
        self.prev_queue = self.queue.copy()
        self.prev_pointer = self.start_pointer
        if not self.is_empty():
            self.queue[self.start_pointer] = None
            self.start_pointer += 1
            return True
        return False

    def peek_queue(self) -> str:
        """Returns the top item of the queue"""
        return self.queue[self.start_pointer]

    def view_queue(self) -> None:
        """Prints the whole queue"""
        for i in range(len(self.queue)):
            print(self.queue[i])

    def is_full(self) -> bool:
        """Returns True if the queue is full (end pointer is past end of queue)"""
        if self.end_pointer >= len(self.queue):
            return True
        else:
            return False

    def is_empty(self) -> bool:
        """Returns True if the queue is empty (has all None types)"""
        if self.start_pointer == self.end_pointer:
            return True
        else:
            return False

    def undo(self) -> None:
        """Reverts queue to the state of prev_queue"""
        self.queue = self.prev_queue.copy()
        self.start_pointer = self.prev_pointer

    def save_queue(self, file_name: str = "") -> bool:
        """Saves queue to a text file. If no file name given, will get user input"""
        if self.is_full():
            if file_name == "":
                file_name = input("Enter file name: ")

            with open(f"{self.root_path}{file_name}.txt", "w") as file:
                file.write(
                    f"{len(self.queue)}\n{self.start_pointer}\n{self.end_pointer}\n"
                )
                for i in self.queue:
                    file.write(f"{i}\n")
            return True
        else:
            return False

    def load_queue(self, file_name: str = "") -> bool:
        """Loads queue from a text file. If no file name given, will get user input"""
        if file_name == "":
            file_name = input("Enter file name: ")

        try:
            with open(f"{self.root_path}{file_name}.txt", "r") as file:
                self.create_queue(int(file.readline().strip()))
                for line in file.readlines():
                    self.enqueue(line.strip())
        except FileNotFoundError:
            return False
        else:
            return True

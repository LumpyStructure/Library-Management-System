from stack import Stack


class DynamicStack(Stack):
    def __init__(self, data: list = []):
        self.pointer = 0
        self.prev_pointer = 0
        self.create_stack()
        for datum in data:
            self.push_stack(datum)

    def create_stack(self):
        """Initialises the stack and prev_stack variables as empty lists"""
        self.stack = []
        self.prev_stack = []

    def push_stack(self, item):
        """Appends the given item to the top of the stack"""
        self.prev_stack = self.stack.copy()
        self.stack.append(item)

    def pop_stack(self) -> bool:
        """Removes the item at the top of the stack if the stack has at least one item in it.
        Returns True if successful and False if not"""
        self.prev_stack = self.stack.copy()
        if len(self.stack) != 0:
            self.stack.pop()
            return True
        else:
            return False

    def is_empty(self) -> bool:
        """Returns True if the stack is empty"""
        if len(self.stack) == 0:
            return True
        else:
            return False

    def is_full(self) -> bool:
        """Always returns False, since the stack can never be full"""
        return False

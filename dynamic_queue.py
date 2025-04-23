from linear_queue import LinearQueue

PATH = "C:/Users/frase/OneDrive - St. John the Baptist School/A-level/Computing/Paper 1 - Programming/Python Programs/Projects/Library Management System"


class DynamicQueue(LinearQueue):
    def __init__(self, root_path=PATH, data=[]):
        self.root_path = root_path
        self.queue = []
        self.prev_queue = []
        self.create_queue()
        for datum in data:
            self.enqueue(datum)

    def create_queue(self):
        """Initialises the queue and prev_queue variables as empty lists"""
        self.queue = []
        self.prev_queue = []

    def enqueue(self, item):
        """Appends the given item to the end of the queue"""
        self.prev_queue = self.queue.copy()
        self.queue.append(item)

    def dequeue(self) -> any:
        """Removes the item at the start of the queue if there is at least one item in the queue.
        Returns the removed item if successful and None if not"""
        self.prev_queue = self.queue.copy()
        if len(self.queue) != 0:
            return self.queue.pop(0)
        else:
            return None

    def peek_queue(self) -> any:
        """Returns the top item of the queue if there is at least one item in the queue.
        If no items in the queue, returns None"""
        if len(self.queue) != 0:
            return self.queue[0]
        else:
            return None

    def is_empty(self) -> bool:
        """Returns True if the queue is empty"""
        if len(self.queue) == 0:
            return True
        else:
            return False

    def is_full(self) -> bool:
        """Always returns False, since the queue can never be full"""
        return False

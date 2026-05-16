import threading
import queue

class EventBus:
    def __init__(self):
        self.queue = queue.Queue()
    def push(self, event: dict):
        self.queue.put(event)
    def listen(self):
        while True:
            yield self.queue.get()
import time


# Timer Class

class Timer:
    def __init__(self, timer):
        self.time = timer
        self.timer = time.time()

    def start_timer(self):
        self.timer = time.time() + self.time

    def update_timer(self, newTime):
        self.time = newTime
        self.timer = time.time() + self.time

    def check_timer(self):
        if self.timer < time.time():
            self.timer = time.time() + self.time
            return True
        return False

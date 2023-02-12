import time

class CountdownTimer:
    def __init__(self, seconds, callback, *args, **kwargs):
        self.seconds = seconds
        self.init_seconds = seconds
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
        """Loop over the timer until it reaches 0"""
        self.seconds = self.init_seconds
        while self.seconds > 0:
            print(self.seconds)
            self.seconds -= 1
            time.sleep(1)
        self.callback(*self.args, **self.kwargs)
        print("Done")
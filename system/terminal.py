import sys
import threading
import time

class Spinner:
    def __init__(self, task_name="Working"):
        self.task_name = task_name
        self.spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.running = False
        self.idx = 0
        self._thread = None

    def start(self):
        self.running = True
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()

    def _spin(self):
        while self.running:
            char = self.spinner_chars[self.idx % len(self.spinner_chars)]
            sys.stdout.write(f"\r{char} {self.task_name}...")
            sys.stdout.flush()
            self.idx += 1
            time.sleep(0.1)

    def stop(self):
        self.running = False
        if self._thread:
            self._thread.join()
        sys.stdout.write(f"\r✔ {self.task_name} done!     \n")
        sys.stdout.flush()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
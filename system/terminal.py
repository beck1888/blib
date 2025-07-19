import sys
import threading
import time

class Cursor:
    @staticmethod
    def show():
        sys.stdout.write("\033[?25h")

    @staticmethod
    def hide():
        sys.stdout.write("\033[?25l")

class Spinner:
    def __init__(self, task_name="Working"):
        self.task_name = task_name
        self.spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.running = False
        self.idx = 0
        self._thread = None
        self.start_time = None  # Track the start time

    def start(self):
        Cursor.hide()  # Hide the cursor when spinner starts
        self.running = True
        self.start_time = time.time()  # Record the start time
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
        if self.start_time:  # Calculate and display elapsed time
            self.elapsed_time = time.time() - self.start_time
            self.elapsed_time = round(self.elapsed_time, 2) # Use an approx

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
        if exc_type is not None:
            # Show the "x" in red
            sys.stdout.write(f"\r\033[31m✖\033[0m {self.task_name} [{self.elapsed_time} s]\n\n") # Provide an empty line for better readability
            # sys.stdout.write(f"{exc_value}\n") # Exception message should be shown automatically by the interpreter, but you can uncomment if this gives issues
            sys.stdout.flush()
        else:
            sys.stdout.write(f"\r\033[32m✔\033[0m {self.task_name} [{self.elapsed_time} s]\n")
            sys.stdout.flush()

        Cursor.show() # Always restore the cursor visibility
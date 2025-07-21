"""
terminal.py

Provides methods for common terminal operations.
"""

import sys
import threading
import time


def show_cursor():
    """Writes the escape code to show the terminal cursor."""
    sys.stdout.write("\033[?25h")

def hide_cursor():
    """Writes the escape code to hide the terminal cursor."""
    sys.stdout.write("\033[?25l")

class Spinner:
    """A simple terminal spinner to indicate ongoing tasks."""

    def __init__(self, task_name="Working"):
        """
        Initialize the spinner with a task name.
        Args:
            task_name (str): The name of the task to display with the spinner.
        """

        self.task_name = task_name
        self.spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.running = False
        self.idx = 0
        self._thread = None
        self.start_time = None  # Track the start time
        self.elapsed_time = 0   # Initialize elapsed time

    def start(self):
        """Start the spinner."""
        hide_cursor()  # Hide the cursor when spinner starts
        self.running = True
        self.start_time = time.time()  # Record the start time
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()

    def _spin(self):
        """The spinning animation that runs in a separate thread."""
        while self.running:
            char = self.spinner_chars[self.idx % len(self.spinner_chars)]
            sys.stdout.write(f"\r{char} {self.task_name}...")
            sys.stdout.flush()
            self.idx += 1
            time.sleep(0.1)

    def stop(self):
        """Stop the spinner."""
        self.running = False
        if self._thread:
            self._thread.join()
        if self.start_time:  # Calculate and display elapsed time
            self.elapsed_time = time.time() - self.start_time
            self.elapsed_time = round(self.elapsed_time, 2) # Use an approx

    def __enter__(self):
        """Start the spinner when entering a context."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Stop the spinner and display the result when exiting a context."""
        try:
            self.stop()
            if exc_type is not None:
                # Show the "x" in red
                sys.stdout.write(f"\r\033[31m✖\033[0m {self.task_name} [{self.elapsed_time} s]\n\n")
                # Provide an empty line for better readability
                # Exception message should be shown automatically by the interpreter
                # You can uncomment if this gives issues
                sys.stdout.flush()
            else:
                sys.stdout.write(f"\r\033[32m✔\033[0m {self.task_name} [{self.elapsed_time} s]\n")
                sys.stdout.flush()
        finally:
            # Make sure the cursor is always shown at the end, even if an error occurs
            show_cursor()
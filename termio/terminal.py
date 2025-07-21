"""
terminal.py

Provides methods for common terminal (stdout) operations.
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

class ColorOut:
    """
    A utility class to print colored text to the terminal using ANSI escape codes.
    """

    COLOR_CODES = {
        "red": "\033[31m",
        "orange": "\033[38;5;208m",  # Approximate orange using 256-color mode
        "yellow": "\033[33m",
        "green": "\033[32m",
        "blue": "\033[34m",
        "purple": "\033[35m",
        "black": "\033[30m",
        "white": "\033[97m",
        "bold": "\033[1m",
        "italics": "\033[3m",
        "strikethrough": "\033[9m",
        "reset": "\033[0m"
    }

    def __init__(self):
        pass

    def _print(self, color_code: str, text: str, newline: bool = True):
        output = f"{self.COLOR_CODES[color_code]}{text}{self.COLOR_CODES['reset']}"
        if newline:
            print(output)
        else:
            print(output, end='')

    def red(self, text: str, newline: bool = True):
        self._print("red", text, newline)

    def orange(self, text: str, newline: bool = True):
        self._print("orange", text, newline)

    def blue(self, text: str, newline: bool = True):
        self._print("blue", text, newline)

    def yellow(self, text: str, newline: bool = True):
        self._print("yellow", text, newline)

    def bold(self, text: str, newline: bool = True):
        self._print("bold", text, newline)

    def green(self, text: str, newline: bool = True):
        self._print("green", text, newline)

    def purple(self, text: str, newline: bool = True):
        self._print("purple", text, newline)

    def black(self, text: str, newline: bool = True):
        self._print("black", text, newline)

    def white(self, text: str, newline: bool = True):
        self._print("white", text, newline)

    def bold(self, text: str, newline: bool = True):
        self._print("bold", text, newline)

    def italics(self, text: str, newline: bool = True):
        self._print("italics", text, newline)

    def strikethrough(self, text: str, newline: bool = True):
        self._print("strikethrough", text, newline)
    

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
"""
terminal.py

Provides methods for common terminal (stdout) operations, including cursor visibility control,
colored text output, and a spinner for indicating ongoing tasks.
"""

import sys
import threading
import time

# Common symbols a dev might want to use
CAUTION = '⚠'
CHECK_MARK = '✔'
X_MARK = '✗'


# Functions
def show_cursor():
    """
    Show the terminal cursor by writing the appropriate escape code.

    This function is useful for restoring the cursor visibility after it has been hidden.
    """
    sys.stdout.write("\033[?25h")

def hide_cursor():
    """
    Hide the terminal cursor by writing the appropriate escape code.

    This function is useful for improving the user experience during animations or spinners.
    """
    sys.stdout.write("\033[?25l")

class ColorOut:
    """
    A utility class to print colored text to the terminal using ANSI escape codes.

    Attributes:
        COLOR_CODES (dict): A dictionary mapping color names and styles to their ANSI codes.
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
        """
        Initialize the ColorOut class.

        This class does not require any specific initialization logic.
        """
        pass

    def _print(self, color_code: str, text: str, newline: bool = True):
        """
        Print text in a specified color or style.

        Args:
            color_code (str): The key from COLOR_CODES representing the desired color or style.
            text (str): The text to be printed.
            newline (bool): Whether to append a newline after the text. Defaults to True.
        """
        output = f"{self.COLOR_CODES[color_code]}{text}{self.COLOR_CODES['reset']}"
        if newline:
            print(output)
        else:
            print(output, end='')

    def red(self, text: str, newline: bool = True):
        """
        Print text in red.

        Args:
            text (str): The text to be printed.
            newline (bool): Whether to append a newline after the text. Defaults to True.
        """
        self._print("red", text, newline)

    def orange(self, text: str, newline: bool = True):
        """
        Print text in orange.

        Args:
            text (str): The text to be printed.
            newline (bool): Whether to append a newline after the text. Defaults to True.
        """
        self._print("orange", text, newline)

    def blue(self, text: str, newline: bool = True):
        """
        Print text in blue.

        Args:
            text (str): The text to be printed.
            newline (bool): Whether to append a newline after the text. Defaults to True.
        """
        self._print("blue", text, newline)

    def yellow(self, text: str, newline: bool = True):
        """
        Print text in yellow.

        Args:
            text (str): The text to be printed.
            newline (bool): Whether to append a newline after the text. Defaults to True.
        """
        self._print("yellow", text, newline)

    def bold(self, text: str, newline: bool = True):
        """
        Print text in bold.

        Args:
            text (str): The text to be printed.
            newline (bool): Whether to append a newline after the text. Defaults to True.
        """
        self._print("bold", text, newline)

    def green(self, text: str, newline: bool = True):
        """
        Print text in green.

        Args:
            text (str): The text to be printed.
            newline (bool): Whether to append a newline after the text. Defaults to True.
        """
        self._print("green", text, newline)

    def purple(self, text: str, newline: bool = True):
        """
        Print text in purple.

        Args:
            text (str): The text to be printed.
            newline (bool): Whether to append a newline after the text. Defaults to True.
        """
        self._print("purple", text, newline)

    def black(self, text: str, newline: bool = True):
        """
        Print text in black.

        Args:
            text (str): The text to be printed.
            newline (bool): Whether to append a newline after the text. Defaults to True.
        """
        self._print("black", text, newline)

    def white(self, text: str, newline: bool = True):
        """
        Print text in white.

        Args:
            text (str): The text to be printed.
            newline (bool): Whether to append a newline after the text. Defaults to True.
        """
        self._print("white", text, newline)

    def bold(self, text: str, newline: bool = True):
        """
        Print text in bold.

        Args:
            text (str): The text to be printed.
            newline (bool): Whether to append a newline after the text. Defaults to True.
        """
        self._print("bold", text, newline)

    def italics(self, text: str, newline: bool = True):
        """
        Print text in italics.

        Args:
            text (str): The text to be printed.
            newline (bool): Whether to append a newline after the text. Defaults to True.
        """
        self._print("italics", text, newline)

    def strikethrough(self, text: str, newline: bool = True):
        """
        Print text with a strikethrough effect.

        Args:
            text (str): The text to be printed.
            newline (bool): Whether to append a newline after the text. Defaults to True.
        """
        self._print("strikethrough", text, newline)
    

class Spinner:
    """
    A simple terminal spinner to indicate ongoing tasks.

    Attributes:
        task_name (str): The name of the task displayed alongside the spinner.
        spinner_chars (list): A list of characters used for the spinner animation.
        running (bool): Whether the spinner is currently running.
        idx (int): The current index in the spinner_chars list.
        _thread (threading.Thread): The thread running the spinner animation.
        start_time (float): The time when the spinner started.
        elapsed_time (float): The total elapsed time the spinner was running.
    """

    def __init__(self, task_name="Working"):
        """
        Initialize the spinner with a task name.

        Args:
            task_name (str): The name of the task to display with the spinner. Defaults to "Working".
        """

        self.task_name = task_name
        self.spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.running = False
        self.idx = 0
        self._thread = None
        self.start_time = None  # Track the start time
        self.elapsed_time = 0   # Initialize elapsed time
        self.ellipsis: str = '...' if not self.task_name.endswith('...') else ''


    def start(self):
        """
        Start the spinner animation in a separate thread.

        This method hides the terminal cursor and begins the spinner animation.
        """
        hide_cursor()  # Hide the cursor when spinner starts
        self.running = True
        self.start_time = time.time()  # Record the start time
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()

    def _spin(self):
        """
        Perform the spinner animation.

        This method runs in a separate thread and updates the spinner character
        in the terminal at regular intervals.
        """
        while self.running:
            char = self.spinner_chars[self.idx % len(self.spinner_chars)]
            sys.stdout.write(f"\r\033[34m{char}\033[0m {self.task_name}{self.ellipsis}")
            sys.stdout.flush()
            self.idx += 1
            time.sleep(0.1)

    def stop(self):
        """
        Stop the spinner animation and calculate the elapsed time.

        This method restores the terminal cursor and stops the spinner thread.
        """
        self.running = False
        if self._thread:
            self._thread.join()
        if self.start_time:  # Calculate and display elapsed time
            self.elapsed_time = time.time() - self.start_time
            self.elapsed_time = round(self.elapsed_time, 2) # Use an approx

    def __enter__(self):
        """
        Start the spinner when entering a context.

        Returns:
            Spinner: The spinner instance.
        """
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Stop the spinner and display the result when exiting a context.

        Args:
            exc_type (type): The exception type, if an exception occurred.
            exc_value (Exception): The exception instance, if an exception occurred.
            traceback (traceback): The traceback object, if an exception occurred.
        """
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
"""
inputs.py

Provides utilities for terminal input with enhanced flexibility.

This module contains:
- get_masked_input: Prompts the user for input with each character masked.
"""

import sys
import tty
import termios

def get_masked_input(prompt: str = "Password: ", mask_char: str = "*") -> str:
    """
    Prompt the user for input from the terminal with each character masked.

    This function is intended for securely gathering sensitive input (like passwords)
    without echoing the actual characters typed. Instead, a masking character (default '*')
    is shown for each typed character. Supports basic backspace handling.

    Args:
        prompt (str): The message to display to the user before input begins.
        mask_char (str): The character to display in place of typed input.

    Returns:
        str: The user input as a plain string (not masked).

    Raises:
        ValueError: If the terminal settings cannot be restored after input.
    """
    sys.stdout.write(prompt)
    sys.stdout.flush()

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    result = []

    try:
        tty.setraw(fd)  # Set terminal to raw mode (character-by-character input)
        while True:
            ch = sys.stdin.read(1)
            if ch in ('\r', '\n'):
                sys.stdout.write('\r\n')  # Move to new line on Enter
                break
            elif ch == '\x7f':  # Handle backspace/delete
                if result:
                    result.pop()
                    sys.stdout.write('\b \b')  # Erase last masked character
            else:
                result.append(ch)
                sys.stdout.write(mask_char)  # Show mask character
            sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  # Restore terminal settings

    return ''.join(result)
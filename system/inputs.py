"""A module for handling user inputs in the terminal."""

import sys
import tty
import termios

def get_masked_input(prompt="Password: ", mask_char="*"):
    """Prompt for input and mask the characters as the user types."""
    sys.stdout.write(prompt)
    sys.stdout.flush()

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    result = []

    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)
            if ch in ('\r', '\n'):
                sys.stdout.write('\r\n')  # Force full carriage return and newline
                break
            elif ch == '\x7f':  # Backspace/delete key
                if result:
                    result.pop()
                    sys.stdout.write('\b \b')  # Backspace, overwrite, backspace again
            else:
                result.append(ch)
                sys.stdout.write(mask_char)
            sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ''.join(result)

"""
applescript_dialogs.py

Provides a pythonic abstraction for showing and interacting with the
macOS GUI popups using Apple Script.
"""

import subprocess
import re
import os

# Private Methods
def __run_applescript(script: str) -> str:
    """
    Executes an AppleScript command using the `osascript` CLI tool.

    Args:
        script (str): The AppleScript code to run.

    Returns:
        str: The standard output from the AppleScript execution, stripped of trailing whitespace.

    Raises:
        RuntimeError: If the AppleScript execution fails.
    """
    try:
        result = subprocess.run(
            ['osascript', '-e', script],
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"AppleScript execution failed: {e.stderr.strip()}")
    

def __sanitize_for_applescript(text: str, max_length: int = 250) -> str:
    """
    Cleans and escapes a string for safe use in AppleScript dialog boxes.

    This includes:
      - Escaping double quotes.
      - Replacing newlines, carriage returns, and tabs with spaces.
      - Removing non-printable characters.
      - Truncating long strings to fit within AppleScript dialog limits.

    Args:
        text (str): The raw string to sanitize.
        max_length (int): Maximum length for the sanitized string (default: 250).

    Returns:
        str: A sanitized, escaped, and truncated version of the input string.
    """
    sanitized = text.replace('"', '\\"')
    sanitized = re.sub(r'[\n\r\t]', ' ', sanitized)
    sanitized = ''.join(c for c in sanitized if c.isprintable())

    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length - 3] + '...'

    return sanitized

# Public methods
def popup_ask_for_input(prompt: str, allow_cancel: bool = False) -> str | None:
    """
    Displays an AppleScript dialog box asking the user for text input.

    Args:
        prompt (str): The message shown to the user.
        allow_cancel (bool): Whether to allow canceling the prompt. If True, returns None on cancel.

    Returns:
        str | None: The user's input as a string, or None if canceled (when `allow_cancel` is True).
    """
    prompt = __sanitize_for_applescript(prompt)

    if allow_cancel:
        script = f'display dialog "{prompt}" default answer "" buttons {{"Cancel", "OK"}} default button "OK"'
    else:
        script = f'display dialog "{prompt}" default answer "" buttons {{"OK"}} default button "OK"'

    try:
        return __run_applescript(script).split(':')[-1]
    except RuntimeError as e:
        if "AppleScript execution failed" in str(e):
            return None
        raise

def popup_show_message(message: str, allow_cancel: bool = False, icon_path: str | None = None) -> bool:
    """
    Displays an AppleScript dialog box with a message and OK/Cancel buttons.
    Optionally displays a custom icon (must be .icns or compatible format).

    Args:
        message (str): The message to display.
        allow_cancel (bool): Whether to include a Cancel button.
        icon_path (str | None): Absolute path to a custom icon file.

    Returns:
        bool: True if the user clicked OK, False if they canceled.
    """
    message = __sanitize_for_applescript(message)

    # Build base AppleScript
    buttons = '{"Cancel", "OK"}' if allow_cancel else '{"OK"}'
    script = f'display dialog "{message}" buttons {buttons} default button "OK"'

    # Add custom icon if provided
    if icon_path:
        if not os.path.exists(icon_path):
            raise FileNotFoundError(f"Path '{icon_path}' doesn't exist.")
        
        icon_path = icon_path.replace('"', '\\"')
        script += f' with icon POSIX file "{icon_path}"'

    try:
        __run_applescript(script)
    except RuntimeError as e:
        if "AppleScript execution failed" in str(e):
            return False
        raise
    return True
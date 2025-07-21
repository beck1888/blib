"""
applescript_dialogs.py

Provides a pythonic abstraction for showing and interacting with the
macOS GUI popups using Apple Script.
"""

import subprocess
import re
import os
from typing import Optional

# Helpers
def __run_applescript(script: str) -> str:
    result = subprocess.run(
        ["osascript", "-e", script],
        stdout=subprocess.PIPE,    # HUSH UP
        stderr=subprocess.DEVNULL, # THAT GOES FOR YOU TOO
        text=True
    )
    return result.stdout.strip()

def __sanitize_for_applescript(text: str, max_length: int = 250) -> str:
    text = text.replace('"', '\\"')
    text = re.sub(r'[\n\r\t]', ' ', text)
    text = ''.join(c for c in text if c.isprintable())
    return text[:max_length - 3] + "..." if len(text) > max_length else text

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

def popup_show_message(
    message: str,
    image_path: Optional[str] = None,
    buttons: list[str] = ["Cancel", "Okay"],
    primary_button: str = "Okay",
    timeout: Optional[int] = None
) -> Optional[str]:
    if not buttons:
        raise ValueError("You must specify at least one button.")
    if primary_button not in buttons:
        raise ValueError(f"Primary button '{primary_button}' must be one of: {buttons}")

    sanitized_msg = __sanitize_for_applescript(message)
    button_str = "{" + ", ".join(f'"{__sanitize_for_applescript(b)}"' for b in buttons) + "}"
    script = f'display dialog "{sanitized_msg}" buttons {button_str} default button "{primary_button}"'

    if image_path:
        full_path = os.path.abspath(image_path)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Image path '{full_path}' does not exist.")
        sanitized_icon = full_path.replace('"', '\\"')
        script += f' with icon POSIX file "{sanitized_icon}"'

    if timeout:
        script += f' giving up after {timeout}'

    # # Make sure we return just the button text
    # script += '\nreturn button returned'

    try:
        result = __run_applescript(script)

        # Get just the button clicked
        start_of_relevant_output = result.find('button returned:') + 16 # Account for length of what we find
        end_of_relevant_output = result.find(',') # First comma separates returned values
        clean_result = result[start_of_relevant_output: end_of_relevant_output].strip() # Why Not

        # Check if the user clicked anything (no timeout)
        if len(clean_result) > 0:
            return clean_result
        else:
            return None
    except subprocess.CalledProcessError:
        return None
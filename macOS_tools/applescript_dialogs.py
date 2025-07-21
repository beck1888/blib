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
    """
    Executes an AppleScript command and returns the output.

    Args:
        script (str): The AppleScript command to execute.

    Returns:
        str: The output of the AppleScript command.

    Raises:
        subprocess.CalledProcessError: If the AppleScript command fails.
    """
    result = subprocess.run(
        ["osascript", "-e", script],
        stdout=subprocess.PIPE,    # HUSH UP
        stderr=subprocess.DEVNULL, # THAT GOES FOR YOU TOO
        text=True
    )
    return result.stdout.strip()

def __sanitize_for_applescript(text: str, max_length: int = 250) -> str:
    """
    Sanitizes a string for use in AppleScript by escaping special characters
    and truncating it to a maximum length.

    Args:
        text (str): The text to sanitize.
        max_length (int): The maximum allowed length of the sanitized text.

    Returns:
        str: The sanitized and truncated text.
    """
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

    Raises:
        RuntimeError: If the AppleScript execution fails.
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
    """
    Displays an AppleScript dialog box with a message and customizable buttons.

    Args:
        message (str): The message to display in the dialog box.
        image_path (Optional[str]): Path to an image to display as an icon. Defaults to None.
        buttons (list[str]): List of button labels to display. Defaults to ["Cancel", "Okay"].
        primary_button (str): The default button to highlight. Defaults to "Okay".
        timeout (Optional[int]): Time in seconds before the dialog auto-closes. Defaults to None.

    Returns:
        Optional[str]: The label of the button clicked by the user, or None if the dialog times out.

    Raises:
        ValueError: If no buttons are provided or the primary button is not in the button list.
        FileNotFoundError: If the specified image path does not exist.
        subprocess.CalledProcessError: If the AppleScript execution fails.
    """
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
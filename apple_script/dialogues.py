"""Class for handling AppleScript dialogues."""

import subprocess

def run_applescript(script: str) -> str:
    """
    Run an AppleScript command and return the output.
    
    :param script: The AppleScript code to execute.
    :return: The output of the AppleScript command.
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
    
import re

def sanitize_for_applescript(text: str, max_length: int = 250) -> str:
    """
    Sanitize input for safe use in AppleScript dialogues.
    
    Escapes double quotes, removes control characters (like newlines),
    trims excessively long strings, and prevents basic AppleScript injection.

    :param text: The input string to sanitize.
    :param max_length: The maximum length of the string.
    :return: A sanitized string safe for AppleScript dialogues.
    """

    # Escape double quotes so AppleScript doesn't break
    sanitized = text.replace('"', '\\"')

    # Replace newlines, carriage returns, tabs with a space
    sanitized = re.sub(r'[\n\r\t]', ' ', sanitized)

    # Remove other non-printable control characters (except standard spaces)
    sanitized = ''.join(c for c in sanitized if c.isprintable())

    # Truncate to reasonable AppleScript dialog limits
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length - 3] + '...'

    return sanitized
    
class AppleScriptDialogues:
    """
    A class to handle AppleScript dialogues for user interaction.
    """

    @staticmethod
    def ask_for_input(prompt: str, allow_cancel: bool = False) -> str | None:
        """
        Ask the user for input using an AppleScript dialogue.
        
        :param prompt: The prompt message to display in the dialogue.
        :param allow_cancel: Whether to allow the user to cancel the input.
        :return: The user's input as a string or None if cancelled.

        Raises:
            RuntimeError: If the AppleScript execution fails.
        """
        # Sanitize the prompt to remove string issues that might cause Apple Script to fail
        prompt = sanitize_for_applescript(prompt)

        if allow_cancel:
            script = f'display dialog "{prompt}" default answer "" buttons {{"Cancel", "OK"}} default button "OK"'
        else:
            script = f'display dialog "{prompt}" default answer "" buttons {{"OK"}} default button "OK"'

        # We need to use try here in case the user cancels the dialogue
        # which will raise a specific RuntimeError
        try:
            # The result is in the format "button returned:OK, text returned:User Input"
            # We need to extract the text returned part
            # So we find the last colon and return everything after it
            return run_applescript(script).split(':')[-1]
        except RuntimeError as e:
            # Catch the specific error for AppleScript execution failure on cancel
            if "AppleScript execution failed" in str(e):
                return None
            # Re-raise if it's not a known error
            raise
    
    @staticmethod
    def show_message(message: str, allow_cancel: bool = False) -> bool:
        """
        Show a message to the user using an AppleScript dialogue.
        
        :param message: The message to display.
        :param allow_cancel: Whether to allow the user to cancel the message.

        :return: bool
            True if the user clicked "OK" (or primary button), False if they clicked "Cancel" (secondary button) (if allowed)

        Raises:
            RuntimeError: If the AppleScript execution fails.
        """
        # Sanitize the prompt to remove string issues that might cause Apple Script to fail
        message = sanitize_for_applescript(message)

        if allow_cancel:
            script = f'display dialog "{message}" buttons {{"Cancel", "OK"}} default button "OK"'
        else:
            script = f'display dialog "{message}" buttons {{"OK"}} default button "OK"'

        try:
            run_applescript(script)
        except RuntimeError as e:
            # Catch the specific error for AppleScript execution failure on cancel
            if "AppleScript execution failed" in str(e):
                return False
            raise  # Re-raise if it's not a known error
        return True
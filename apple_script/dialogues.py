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
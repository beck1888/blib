import subprocess
import re

# Private Methods
def __run_applescript(script: str) -> str:
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

# Public methods
def ask_for_input(prompt: str, allow_cancel: bool = False) -> str | None:
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

def show_message(message: str, allow_cancel: bool = False) -> bool:
    message = __sanitize_for_applescript(message)

    if allow_cancel:
        script = f'display dialog "{message}" buttons {{"Cancel", "OK"}} default button "OK"'
    else:
        script = f'display dialog "{message}" buttons {{"OK"}} default button "OK"'

    try:
        __run_applescript(script)
    except RuntimeError as e:
        if "AppleScript execution failed" in str(e):
            return False
        raise
    return True

import subprocess
import os

def take_screenshot(file_path: str) -> str:
    """
    Takes a screenshot on macOS and saves it as a PNG to the specified file path.

    :param file_path: The absolute or relative path where the screenshot will be saved.
    :returns str: The file path where the image eas saved.
    :raises FileExistsError: If the file already exists at the given path.
    :raises RuntimeError: If the screenshot command fails.
    """
    # Expand and validate the full path
    file_path = os.path.abspath(file_path)

    if os.path.exists(file_path):
        raise FileExistsError(f"File already exists: {file_path}")
    
    if not file_path.endswith(".png"):
        raise ValueError("The filepath must end in .png")

    try:
        subprocess.run(
            ["screencapture", "-x", file_path],
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Screenshot failed: {e}")


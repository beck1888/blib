"""
screenshot.py

Provides a utility function to capture screenshots on macOS and save them as PNG files.
"""

import subprocess
import os

def take_screenshot(file_path: str) -> str:
    """
    Captures a screenshot on macOS and saves it as a PNG file to the specified path.

    Args:
        file_path (str): The absolute or relative path where the screenshot will be saved. 
                         Must end with ".png".

    Returns:
        str: The file path where the screenshot was saved.

    Raises:
        FileExistsError: If a file already exists at the specified path.
        ValueError: If the file path does not end with ".png".
        RuntimeError: If the screenshot command fails.
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


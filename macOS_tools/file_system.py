"""
file_system.py

Provides utility functions for file system operations, such as creating sparse files.
"""

import os

def create_fake_file_of_size(file_path: str, size_in_mb: int) -> None:
    """
    Creates a sparse file at the specified path with the given size in megabytes.

    Args:
        file_path (str): The absolute or relative path of the file to create.
        size_in_mb (int): The size of the file in megabytes.

    Returns:
        None

    Raises:
        ValueError: If the size is negative.
        OSError: If there is an issue creating the file.
    """
    if size_in_mb < 0:
        raise ValueError("Size must be a non-negative integer.")
    
    size_in_bytes = size_in_mb * 1000 * 1000
    with open(file_path, 'wb') as f:
        f.seek(size_in_bytes - 1)
        f.write(b'\0')

"""
local.py

Provides a utility function to retrieve the user's local IP address.
"""

import socket

def get_user_ip() -> str:
    """
    Retrieve the user's local IP address.

    This function determines the local IP address by creating a UDP connection
    to a public server (Google's public DNS at 8.8.8.8) and retrieving the
    socket's local address.

    Returns:
        str: The local IP address of the user, or an error message if retrieval fails.

    Raises:
        Exception: If there is an error during the socket operation.
    """
    try:
        # Connect to a public server to determine the local IP address
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception as e:
        return f"Error retrieving IP: {e}"
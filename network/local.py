import socket

def get_user_ip() -> str:
    """
    Get the user's IP address.

    Returns:
        str: The IP address of the user.
    """
    try:
        # Connect to a public server to determine the local IP address
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception as e:
        return f"Error retrieving IP: {e}"
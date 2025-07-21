import socket

def is_online(timeout=3) -> bool:
    """
    Check if the computer is connected to the internet.

    This function attempts to establish a TCP connection to a known reliable
    server (Google's public DNS at 8.8.8.8 on port 53) to determine if the
    machine has internet access.

    Parameters:
        timeout (int): The timeout in seconds for the connection attempt.

    Returns:
        bool: True if the connection was successful (i.e., online), False otherwise.

    Raises:
        None
    """
    try:
        socket.setdefaulttimeout(timeout)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(("8.8.8.8", 53))
        return True
    except OSError:
        return False
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
    

def is_site_reachable(hostname, port=80, timeout=3):
    """
    Check if a specific site or server is reachable over the network.

    Attempts to resolve the hostname and establish a TCP connection to the
    given port (default is 80 for HTTP).

    Parameters:
        hostname (str): The hostname or IP address of the site.
        port (int): The port number to connect to (default is 80).
        timeout (int): Timeout in seconds for the connection attempt.

    Returns:
        bool: True if the site is reachable, False otherwise.

    Raises:
        None
    """
    try:
        socket.setdefaulttimeout(timeout)
        with socket.create_connection((hostname, port), timeout):
            return True
    except (socket.timeout, socket.gaierror, socket.error):
        return False
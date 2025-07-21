import socket
from urllib.parse import urlparse

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

def is_site_reachable(url_or_hostname, port=None, timeout=3):
    """
    Check if a site is reachable. Accepts either a plain hostname or a full URL.

    Parameters:
        url_or_hostname (str): A domain name or full URL.
        port (int, optional): Port number to use (defaults to 443 for HTTPS, 80 for HTTP).
        timeout (int): Timeout in seconds for the connection attempt.

    Returns:
        bool: True if the site is reachable, False otherwise.
    """
    try:
        # Parse URL if scheme is present
        parsed = urlparse(url_or_hostname)
        hostname = parsed.hostname or url_or_hostname
        port = port or (443 if parsed.scheme == 'https' else 80)

        socket.setdefaulttimeout(timeout)
        with socket.create_connection((hostname, port), timeout):
            return True
    except (socket.timeout, socket.gaierror, socket.error, ValueError):
        return False
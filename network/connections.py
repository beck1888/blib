"""
connections.py

Provides utility functions to check internet connectivity and site reachability.

This module contains:
- is_online: Checks if the computer is connected to the internet.
- is_site_reachable: Checks if a specific site or URL is reachable.
"""

import socket
from urllib.parse import urlparse

def is_online(timeout=3) -> bool:
    """
    Check if the computer is connected to the internet.

    This function attempts to establish a TCP connection to a known reliable
    server (Google's public DNS at 8.8.8.8 on port 53) to determine if the
    machine has internet access.

    Args:
        timeout (int): The timeout in seconds for the connection attempt.

    Returns:
        bool: True if the connection was successful (i.e., online), False otherwise.
    """
    try:
        socket.setdefaulttimeout(timeout)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(("8.8.8.8", 53))
        return True
    except OSError:
        return False

def is_site_reachable(url_or_hostname: str, port: int = None, timeout: int = 3) -> bool:
    """
    Check if a site is reachable. Accepts either a plain hostname or a full URL.

    Args:
        url_or_hostname (str): A domain name or full URL to check.
        port (int, optional): Port number to use (defaults to 443 for HTTPS, 80 for HTTP).
        timeout (int): Timeout in seconds for the connection attempt.

    Returns:
        bool: True if the site is reachable, False otherwise.

    Raises:
        ValueError: If the provided URL or hostname is invalid.
        socket.timeout: If the connection attempt times out.
        socket.gaierror: If the hostname cannot be resolved.
        socket.error: For other socket-related errors.
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
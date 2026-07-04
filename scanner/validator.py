"""
validator.py

Input validation for PortScanner Pro.
"""

import ipaddress
import socket


class Validator:

    @staticmethod
    def validate_target(target: str) -> bool:
        """
        Accepts either an IP address or a hostname.
        """

        try:
            ipaddress.ip_address(target)
            return True
        except ValueError:
            pass

        try:
            socket.gethostbyname(target)
            return True
        except socket.gaierror:
            return False

    @staticmethod
    def validate_port(port: int) -> bool:
        return 1 <= port <= 65535
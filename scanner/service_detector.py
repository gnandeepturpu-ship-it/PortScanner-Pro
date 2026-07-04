"""
service_detector.py

Maps common TCP ports to service names.
"""

import socket


class ServiceDetector:

    @staticmethod
    def get_service(port: int) -> str:
        """
        Return the service name for a port.
        """

        try:
            return socket.getservbyport(port, "tcp").upper()
        except OSError:
            return "UNKNOWN"
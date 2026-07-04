"""
tcp_scanner.py

Core TCP Scanner
"""

import socket


class TCPScanner:

    def __init__(self, timeout=1.0):
        self.timeout = timeout

    def scan_port(self, target, port):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)

        try:

            result = sock.connect_ex((target, port))

            if result == 0:
                return {
                    "port": port,
                    "status": "Open"
                }

            return {
                "port": port,
                "status": "Closed"
            }

        except Exception:
            return {
                "port": port,
                "status": "Closed"
            }

        finally:
            sock.close()
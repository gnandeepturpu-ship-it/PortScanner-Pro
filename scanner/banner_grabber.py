"""
banner_grabber.py

Attempts to retrieve a service banner from an open TCP port.
"""

import socket


class BannerGrabber:

    def __init__(self, timeout=2):
        self.timeout = timeout

    def grab_banner(self, target, port):

        try:

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

                sock.settimeout(self.timeout)

                sock.connect((target, port))

                try:
                    sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                except Exception:
                    pass

                banner = sock.recv(1024).decode(
                    errors="ignore"
                ).strip()

                if banner:
                    return banner.replace("\r", " ").replace("\n", " ")

        except Exception:
            pass

        return "No Banner"
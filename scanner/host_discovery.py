"""
host_discovery.py

Host reachability checks for ReconX.
"""

import socket


class HostDiscovery:

    @staticmethod
    def is_host_alive(target: str, timeout: float = 2.0):
        """
        Checks if the host is reachable by resolving DNS and attempting
        a TCP connection on common ports.

        Returns:
            (True/False, resolved_ip)
        """

        try:
            ip = socket.gethostbyname(target)

            common_ports = [80, 443, 22]

            for port in common_ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(timeout)

                    if sock.connect_ex((ip, port)) == 0:
                        sock.close()
                        return True, ip

                    sock.close()

                except Exception:
                    pass

            return True, ip

        except Exception:
            return False, None
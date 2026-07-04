"""
port_range.py
"""


class PortRange:

    @staticmethod
    def generate(start_port: int, end_port: int):

        return range(start_port, end_port + 1)
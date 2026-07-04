"""
terminal_ui.py

Professional terminal interface for ReconX.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class TerminalUI:

    @staticmethod
    def show_banner():

        console.print(
            Panel.fit(
                "[bold cyan]RECONX[/bold cyan]\n"
                "[green]Advanced Network Reconnaissance Suite[/green]"
            )
        )

    @staticmethod
    def show_results(open_ports):

        table = Table(title="Open Ports")

        table.add_column("Port", style="cyan")

        table.add_column("Service", style="green")

        table.add_column("Status", style="red")

        for item in open_ports:

            table.add_row(
                str(item["port"]),
                item["service"],
                "OPEN"
            )

        console.print(table)
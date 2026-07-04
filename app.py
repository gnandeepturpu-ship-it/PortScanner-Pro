from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from scanner.host_discovery import HostDiscovery
from scanner.scanner_engine import ScannerEngine
from scanner.validator import Validator

from reports.csv_export import CSVExporter
from reports.json_export import JSONExporter
from reports.html_report import HTMLExporter

console = Console()


def main():

    console.print(
        Panel.fit(
            "[bold cyan]PortScanner-Pro v1.0[/bold cyan]\n"
            "[green]Advanced Multi-Threaded Network Port Scanner[/green]"
        )
    )

    target = console.input("\n[cyan]Target Host/IP : [/cyan]")

    if not Validator.validate_target(target):
        console.print("[bold red]❌ Invalid Target[/bold red]")
        return

    console.print("\n[yellow]Checking host...[/yellow]")

    alive, ip = HostDiscovery.is_host_alive(target)

    if not alive:
        console.print("[bold red]❌ Host appears unreachable[/bold red]")
        return

    console.print("[bold green]✅ Host Online[/bold green]")
    console.print(f"[cyan]Resolved IP :[/cyan] {ip}")

    start_port = int(console.input("\n[cyan]Start Port : [/cyan]"))
    end_port = int(console.input("[cyan]End Port   : [/cyan]"))

    total_ports = (end_port - start_port) + 1

    engine = ScannerEngine(threads=50)

    results, elapsed = engine.run(
        ip,
        start_port,
        end_port
    )

    table = Table(
        title="PortScanner-Pro Scan Results",
        show_lines=True
    )

    table.add_column("Port", style="cyan", justify="center")
    table.add_column("Service", style="green")
    table.add_column("Banner", style="white")

    for item in results:

        banner = item["banner"]

        if len(banner) > 60:
            banner = banner[:60] + "..."

        table.add_row(
            str(item["port"]),
            item["service"],
            banner
        )

    console.print(table)

    summary = Table(title="Scan Summary")

    summary.add_column("Property", style="cyan")
    summary.add_column("Value", style="green")

    summary.add_row("Target", target)
    summary.add_row("Resolved IP", ip)
    summary.add_row("Open Ports", str(len(results)))
    summary.add_row("Elapsed Time", f"{elapsed:.2f} seconds")

    console.print(summary)

    # -------------------------
    # Scan Statistics
    # -------------------------

    stats = Table(title="Scan Statistics")

    stats.add_column("Metric", style="yellow")
    stats.add_column("Value", style="cyan")

    closed_ports = total_ports - len(results)

    speed = total_ports / elapsed if elapsed > 0 else 0

    stats.add_row("Ports Scanned", str(total_ports))
    stats.add_row("Open Ports", str(len(results)))
    stats.add_row("Closed Ports", str(closed_ports))
    stats.add_row("Scan Speed", f"{speed:.2f} Ports/sec")
    stats.add_row("Threads Used", "50")

    console.print(stats)

    csv_file = CSVExporter.export(results, target)
    json_file = JSONExporter.export(results, target)
    html_file = HTMLExporter.export(results, target, elapsed)

    console.print(
        Panel.fit(
            "[bold green]Reports Generated Successfully[/bold green]"
        )
    )

    console.print(f"📄 CSV  : [green]{csv_file}[/green]")
    console.print(f"📄 JSON : [green]{json_file}[/green]")
    console.print(f"📄 HTML : [green]{html_file}[/green]")


if __name__ == "__main__":
    main()
"""
scanner_engine.py

PortScanner-Pro scanning engine with Rich Progress Bar.
"""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeElapsedColumn
)

from scanner.banner_grabber import BannerGrabber
from scanner.port_range import PortRange
from scanner.service_detector import ServiceDetector
from scanner.tcp_scanner import TCPScanner


class ScannerEngine:

    def __init__(self, threads=50):

        self.threads = threads
        self.scanner = TCPScanner()
        self.banner = BannerGrabber()

    def run(self, target, start_port, end_port):

        start_time = time.time()

        results = []

        ports = list(PortRange.generate(start_port, end_port))

        print()

        with Progress(
            SpinnerColumn(),
            TextColumn("[cyan]Scanning Ports..."),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            TimeElapsedColumn(),
        ) as progress:

            task = progress.add_task(
                "scan",
                total=len(ports)
            )

            with ThreadPoolExecutor(max_workers=self.threads) as executor:

                futures = {
                    executor.submit(
                        self.scanner.scan_port,
                        target,
                        port
                    ): port
                    for port in ports
                }

                for future in as_completed(futures):

                    result = future.result()

                    progress.update(task, advance=1)

                    if result["status"] == "Open":

                        port = result["port"]

                        service = ServiceDetector.get_service(port)

                        banner = self.banner.grab_banner(
                            target,
                            port
                        )

                        results.append({
                            "port": port,
                            "service": service,
                            "banner": banner
                        })

        results.sort(key=lambda x: x["port"])

        elapsed = time.time() - start_time

        return results, elapsed
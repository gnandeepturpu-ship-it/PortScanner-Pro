"""
csv_export.py

Exports scan results to CSV.
"""

import csv
import os
from datetime import datetime


class CSVExporter:

    @staticmethod
    def export(results, target):

        os.makedirs("exports", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = f"exports/{target.replace('.', '_')}_{timestamp}.csv"

        with open(filename, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Port",
                "Service",
                "Banner"
            ])

            for item in results:

                writer.writerow([
                    item["port"],
                    item["service"],
                    item["banner"]
                ])

        return filename
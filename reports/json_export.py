"""
json_export.py

Exports scan results to JSON.
"""

import json
import os
from datetime import datetime


class JSONExporter:

    @staticmethod
    def export(results, target):

        os.makedirs("exports", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = f"exports/{target.replace('.', '_')}_{timestamp}.json"

        data = {
            "target": target,
            "total_open_ports": len(results),
            "scan_results": results
        }

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        return filename
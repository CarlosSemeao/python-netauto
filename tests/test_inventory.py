from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from netauto_training.inventory import process_inventory


class TestInventoryProcessing(unittest.TestCase):
    def test_process_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            input_file = temp_path / "devices.csv"
            valid_output_file = temp_path / "valid_devices.csv"
            invalid_output_file = temp_path / "invalid_devices.txt"

            input_file.write_text(
                (
                    "hostname,ip_address,role,site\n"
                    "r1,10.1.1.1,router,london\n"
                    "r2,300.1.1.1,router,london\n"
                    ",10.1.1.2,switch,paris\n"
                    "sw1,10.1.1.3,switch,paris\n"
                ),
                encoding="utf-8",
            )

            valid_count, invalid_count = process_inventory(
                input_file=input_file,
                valid_output_file=valid_output_file,
                invalid_output_file=invalid_output_file,
            )

            assert valid_count == 2
            assert invalid_count == 2

            with valid_output_file.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            assert len(rows) == 2
            assert rows[0]["hostname"] == "r1"
            assert rows[1]["hostname"] == "sw1"

            invalid_lines = invalid_output_file.read_text(encoding="utf-8").splitlines()
            assert len(invalid_lines) == 2
            assert "invalid ip" in invalid_lines[0]
            assert "missing required field" in invalid_lines[1]


if __name__ == "__main__":
    unittest.main()

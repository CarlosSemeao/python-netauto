from __future__ import annotations
import json
import tempfile
import unittest
from pathlib import Path
from netauto_training.inventory_summary import load_valid_devices, build_site_summary, write_site_summary, write_backup_commands

class TestInventorySummary(unittest.TestCase):
    def test_summary_and_backup_plan(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            input_file = temp_path / "devices.csv"
            summary_file = temp_path / "site_summary.json"
            backup_file = temp_path / "backup_commands.txt"

            input_file.write_text(
                "hostname,ip_address,role,site\n"
                "r1,10.0.0.1,router,london\n"
                "sw1,10.0.0.2,switch,london\n"
                "fw1,10.0.1.1,firewall,dublin\n"
                "bad,999.1.1.1,router,london\n",
                encoding="utf-8",
            )

            devices = load_valid_devices(input_file)
            self.assertEqual(len(devices), 3)

            summary = build_site_summary(devices)
            self.assertEqual(summary["london"]["device_count"], 2)
            self.assertEqual(summary["london"]["roles"]["router"], 1)

            write_site_summary(summary, summary_file)
            write_backup_commands(devices, backup_file)

            written_summary = json.loads(summary_file.read_text(encoding="utf-8"))
            self.assertEqual(sorted(written_summary.keys()), ["dublin", "london"])

            lines = backup_file.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 3)
            self.assertIn('ssh admin@10.0.0.1 "show running-config" > backups/london/r1.cfg', lines)

if __name__ == "__main__":
    unittest.main()

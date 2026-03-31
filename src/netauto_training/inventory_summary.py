from __future__ import annotations
import csv
import json
from pathlib import Path
from netauto_training.inventory import INPUT_FILE, OUTPUT_DIR, validate_row

SITE_SUMMARY_FILE = OUTPUT_DIR / "site_summary.json"
BACKUP_COMMANDS_FILE = OUTPUT_DIR / "backup_commands.txt"

def load_valid_devices(input_file: Path = INPUT_FILE) -> list[dict[str, str]]:
    valid_devices = []
    with input_file.open("r", encoding="utf-8", newline="") as handle:
        for row_number, row in enumerate(csv.DictReader(handle), start=2):
            normalized_row = {key: value.strip() for key, value in row.items()}
            is_valid, _ = validate_row(normalized_row, row_number)
            if is_valid:
                valid_devices.append(normalized_row)
    return valid_devices

def build_site_summary(devices: list[dict[str, str]]) -> dict[str, dict[str, object]]:
    summary = {}
    for device in devices:
        site = device["site"]
        if site not in summary:
            summary[site] = {"device_count": 0, "roles": {}, "hostnames": []}
        summary[site]["device_count"] += 1
        summary[site]["roles"][device["role"]] = summary[site]["roles"].get(device["role"], 0) + 1
        summary[site]["hostnames"].append(device["hostname"])
    for site_data in summary.values():
        site_data["hostnames"].sort()
    return dict(sorted(summary.items()))

def write_site_summary(summary, output_file: Path = SITE_SUMMARY_FILE) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)

def write_backup_commands(devices, output_file: Path = BACKUP_COMMANDS_FILE) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8") as handle:
        for device in sorted(devices, key=lambda item: item["hostname"]):
            handle.write(f'ssh admin@{device["ip_address"]} "show running-config" > backups/{device["site"]}/{device["hostname"]}.cfg\n')

def main() -> None:
    devices = load_valid_devices()
    summary = build_site_summary(devices)
    write_site_summary(summary)
    write_backup_commands(devices)
    print(f"Loaded {len(devices)} valid devices across {len(summary)} sites")
    print("Wrote data/output/site_summary.json")
    print("Wrote data/output/backup_commands.txt")

if __name__ == "__main__":
    main()

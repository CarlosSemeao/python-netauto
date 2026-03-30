from __future__ import annotations

import csv
import ipaddress
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_FILE = BASE_DIR / "data" / "input" / "devices.csv"
OUTPUT_DIR = BASE_DIR / "data" / "output"
VALID_OUTPUT_FILE = OUTPUT_DIR / "valid_devices.csv"
INVALID_OUTPUT_FILE = OUTPUT_DIR / "invalid_devices.txt"
REQUIRED_FIELDS = ("hostname", "ip_address", "role", "site")


def validate_row(row: dict[str, str], row_number: int) -> tuple[bool, str]:
    for field in REQUIRED_FIELDS:
        if not row.get(field, "").strip():
            return False, f"row {row_number}: missing required field '{field}'"

    try:
        ipaddress.ip_address(row["ip_address"].strip())
    except ValueError:
        return False, f"row {row_number}: invalid ip '{row['ip_address']}'"

    return True, ""


def process_inventory(
    input_file: Path = INPUT_FILE,
    valid_output_file: Path = VALID_OUTPUT_FILE,
    invalid_output_file: Path = INVALID_OUTPUT_FILE,
) -> tuple[int, int]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    valid_rows: list[dict[str, str]] = []
    invalid_rows: list[str] = []

    with input_file.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)

        for row_number, row in enumerate(reader, start=2):
            normalized_row = {key: value.strip() for key, value in row.items()}
            is_valid, reason = validate_row(normalized_row, row_number)

            if is_valid:
                valid_rows.append(normalized_row)
            else:
                invalid_rows.append(f"{reason} | {normalized_row}")

    with valid_output_file.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(REQUIRED_FIELDS))
        writer.writeheader()
        writer.writerows(valid_rows)

    with invalid_output_file.open("w", encoding="utf-8") as handle:
        for invalid_row in invalid_rows:
            handle.write(f"{invalid_row}\n")

    return len(valid_rows), len(invalid_rows)


def main() -> None:
    valid_count, invalid_count = process_inventory()
    total_count = valid_count + invalid_count

    print(f"Processed {total_count} rows: {valid_count} valid, {invalid_count} invalid")
    print("Wrote data/output/valid_devices.csv")
    print("Wrote data/output/invalid_devices.txt")


if __name__ == "__main__":
    main()

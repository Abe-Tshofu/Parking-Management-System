from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from models import Mall, ParkingRecord, PaymentRecord, User

DATA_DIR = Path(__file__).resolve().parent / "data"
USERS_FILE = DATA_DIR / "users.txt"
MALLS_FILE = DATA_DIR / "malls.txt"
RECORDS_FILE = DATA_DIR / "parking_records.txt"
PAYMENTS_FILE = DATA_DIR / "payments.txt"


def ensure_data_files() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    for file_path in (USERS_FILE, MALLS_FILE, RECORDS_FILE, PAYMENTS_FILE):
        if not file_path.exists():
            file_path.write_text("", encoding="utf-8")

    if USERS_FILE.read_text(encoding="utf-8").strip() == "":
        default_users = [
            User("admin", "admin123", "admin", "Mall Administrator").to_dict(),
            User("owner", "owner123", "owner", "Mall Owner").to_dict(),
        ]
        write_json_lines(USERS_FILE, default_users)

    if MALLS_FILE.read_text(encoding="utf-8").strip() == "":
        default_malls = [
            Mall("Gateway Theatre of Shopping", "flat", 15.00, 250).to_dict(),
            Mall("Pavilion Shopping Centre", "hourly", 10.00, 180).to_dict(),
            Mall("La Lucia Mall", "hourly_capped", 12.00, 150).to_dict(),
        ]
        write_json_lines(MALLS_FILE, default_malls)


def write_json_lines(file_path: Path, items: list[dict[str, Any]]) -> None:
    with file_path.open("w", encoding="utf-8") as file:
        if items:
            for item in items:
                file.write(json.dumps(item) + "\n")


def read_json_lines(file_path: Path) -> list[dict[str, Any]]:
    if not file_path.exists():
        return []

    items: list[dict[str, Any]] = []
    with file_path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if line:
                try:
                    item = json.loads(line)
                except json.JSONDecodeError as error:
                    raise ValueError(
                        f"Invalid JSON in {file_path.name} on line {line_number}: {error.msg}"
                    ) from error
                if not isinstance(item, dict):
                    raise ValueError(
                        f"Invalid data in {file_path.name} on line {line_number}: expected a JSON object."
                    )
                items.append(item)
    return items


def load_users() -> list[User]:
    ensure_data_files()
    return [User.from_dict(item) for item in read_json_lines(USERS_FILE)]


def save_users(users: list[User]) -> None:
    ensure_data_files()
    write_json_lines(USERS_FILE, [user.to_dict() for user in users])


def load_malls() -> list[Mall]:
    ensure_data_files()
    return [Mall.from_dict(item) for item in read_json_lines(MALLS_FILE)]


def save_malls(malls: list[Mall]) -> None:
    ensure_data_files()
    write_json_lines(MALLS_FILE, [mall.to_dict() for mall in malls])


def load_parking_records() -> list[ParkingRecord]:
    ensure_data_files()
    return [ParkingRecord.from_dict(item) for item in read_json_lines(RECORDS_FILE)]


def save_parking_records(records: list[ParkingRecord]) -> None:
    ensure_data_files()
    write_json_lines(RECORDS_FILE, [record.to_dict() for record in records])


def load_payments() -> list[PaymentRecord]:
    ensure_data_files()
    return [PaymentRecord.from_dict(item) for item in read_json_lines(PAYMENTS_FILE)]


def save_payments(payments: list[PaymentRecord]) -> None:
    ensure_data_files()
    write_json_lines(PAYMENTS_FILE, [payment.to_dict() for payment in payments])

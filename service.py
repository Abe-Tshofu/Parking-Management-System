from __future__ import annotations

import math
from datetime import datetime
from typing import Any

from models import Mall, ParkingRecord, PaymentRecord, User
from storage import (
    load_malls,
    load_parking_records,
    load_payments,
    load_users,
    save_parking_records,
    save_payments,
    save_users,
)


class ParkingService:
    def __init__(self) -> None:
        self.users = load_users()
        self.malls = load_malls()
        self.records = load_parking_records()
        self.payments = load_payments()

    def find_user(self, username: str) -> User | None:
        for user in self.users:
            if user.username.lower() == username.lower():
                return user
        return None

    def register_customer(self, username: str, password: str, full_name: str) -> str:
        username = username.strip()
        password = password.strip()
        full_name = full_name.strip()

        if not username or not password or not full_name:
            return "All fields are required."
        if not all(character.isalnum() or character in "._-" for character in username):
            return "Username may contain only letters, numbers, periods, underscores, and hyphens."
        if len(username) < 3 or len(username) > 30:
            return "Username must be between 3 and 30 characters."
        if len(password) < 4:
            return "Password must contain at least 4 characters."
        if len(full_name) > 100 or any(ord(character) < 32 for character in full_name):
            return "Full name must be 100 characters or fewer and contain no control characters."
        if self.find_user(username):
            return "That username already exists."

        customer = User(username=username, password=password, role="customer", full_name=full_name)
        self.users.append(customer)
        save_users(self.users)
        return "Customer registered successfully."

    def login(self, username: str, password: str) -> User | None:
        username = username.strip()
        if not username or not password:
            return None
        user = self.find_user(username)
        if user and user.password == password:
            return user
        return None

    def get_mall(self, mall_name: str) -> Mall | None:
        for mall in self.malls:
            if mall.name.lower() == mall_name.lower():
                return mall
        return None

    def list_malls(self) -> list[Mall]:
        return self.malls

    def calculate_fee(self, mall_name: str, duration_minutes: int) -> float:
        mall = self.get_mall(mall_name)
        if not mall:
            raise ValueError("Mall not found.")
        if isinstance(duration_minutes, bool) or not isinstance(duration_minutes, int) or duration_minutes <= 0:
            raise ValueError("Parking duration must be a positive whole number of minutes.")
        if not math.isfinite(mall.rate) or mall.rate < 0:
            raise ValueError(f"{mall.name} has an invalid parking rate.")

        if mall.pricing_type == "flat":
            return float(mall.rate)
        if mall.pricing_type == "hourly":
            return round(mall.rate * math.ceil(duration_minutes / 60), 2)
        if mall.pricing_type == "hourly_capped":
            raw_charge = mall.rate * math.ceil(duration_minutes / 60)
            return round(min(raw_charge, 60.00), 2)

        raise ValueError(f"{mall.name} has an unsupported pricing rule.")

    def active_vehicle_records(self) -> list[ParkingRecord]:
        return [record for record in self.records if record.status == "parked"]

    def get_parked_vehicle_record(self, vehicle_registration: str) -> ParkingRecord | None:
        for record in self.records:
            if record.vehicle_registration.lower() == vehicle_registration.lower() and record.status == "parked":
                return record
        return None

    def enter_vehicle(self, username: str, mall_name: str, vehicle_registration: str) -> str:
        user = self.find_user(username)
        if not user or user.role != "customer":
            return "A valid customer account is required to enter a vehicle."

        mall = self.get_mall(mall_name)
        if not mall:
            return "Mall not found."

        vehicle_registration = vehicle_registration.strip().upper()
        if not vehicle_registration:
            return "Vehicle registration is required."
        if len(vehicle_registration) > 20 or any(
            not (character.isalnum() or character in " -") for character in vehicle_registration
        ):
            return "Vehicle registration must be 20 characters or fewer and use only letters, numbers, spaces, or hyphens."
        if self.get_parked_vehicle_record(vehicle_registration):
            return "This vehicle is already parked in a mall."

        active_count = len(self.active_vehicle_records())
        if active_count >= sum(item.capacity for item in self.malls):
            return "All parking bays are currently full."

        current_mall_count = sum(
            1 for record in self.records if record.mall_name.lower() == mall.name.lower() and record.status == "parked"
        )
        if current_mall_count >= mall.capacity:
            return f"{mall.name} has reached maximum capacity."

        record = ParkingRecord(
            record_id=f"REC-{len(self.records) + 1:05d}",
            vehicle_registration=vehicle_registration,
            customer_username=username,
            mall_name=mall.name,
            entry_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status="parked",
        )
        self.records.append(record)
        save_parking_records(self.records)
        return f"Vehicle {vehicle_registration} entered {mall.name} successfully."

    def exit_vehicle(self, username: str, vehicle_registration: str) -> str:
        user = self.find_user(username)
        if not user or user.role != "customer":
            return "A valid customer account is required to exit a vehicle."

        vehicle_registration = vehicle_registration.strip().upper()
        if not vehicle_registration:
            return "Vehicle registration is required."

        record = self.get_parked_vehicle_record(vehicle_registration)
        if not record:
            return "No active parking record was found for that vehicle."
        if record.customer_username.lower() != user.username.lower():
            return "You can only exit a vehicle registered to your customer account."

        exit_time = datetime.now()
        try:
            entry_time = datetime.strptime(record.entry_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return f"Cannot exit {vehicle_registration}: its saved entry time is invalid."
        if entry_time > exit_time:
            return f"Cannot exit {vehicle_registration}: its entry time is in the future."
        duration_minutes = max(int((exit_time - entry_time).total_seconds() // 60), 1)
        fee = self.calculate_fee(record.mall_name, duration_minutes)

        record.exit_time = exit_time.strftime("%Y-%m-%d %H:%M:%S")
        record.duration_minutes = duration_minutes
        record.fee_amount = fee
        record.status = "completed"
        save_parking_records(self.records)
        return (
            f"Vehicle {vehicle_registration} exited successfully. "
            f"Parking duration: {duration_minutes} minutes. "
            f"Fee due: R{fee:.2f}."
        )

    def outstanding_fees(self, username: str) -> list[ParkingRecord]:
        return [
            record
            for record in self.records
            if record.customer_username.lower() == username.lower()
            and record.status == "completed"
            and record.fee_amount > record.paid_amount
        ]

    def payment_history(self, username: str) -> list[PaymentRecord]:
        return [payment for payment in self.payments if payment.username.lower() == username.lower()]

    def record_payment(self, username: str, vehicle_registration: str, amount: float) -> str:
        customer = self.find_user(username)
        if not customer or customer.role != "customer":
            return "A valid customer account is required to make a payment."

        vehicle_registration = vehicle_registration.strip().upper()
        if not vehicle_registration:
            return "Vehicle registration is required."
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            return "Payment amount must be a valid number."
        if not math.isfinite(amount):
            return "Payment amount must be a finite number."
        amount = round(amount, 2)
        if amount <= 0:
            return "Payment amount must be greater than zero."
        matched_records = [
            record
            for record in self.records
            if record.customer_username.lower() == username.lower()
            and record.vehicle_registration.lower() == vehicle_registration.lower()
            and record.status == "completed"
            and record.fee_amount > record.paid_amount
        ]

        if not matched_records:
            return "No unpaid parking fees were found for that vehicle."

        amount_remaining = sum(record.fee_amount - record.paid_amount for record in matched_records)
        if amount > amount_remaining:
            return f"Payment exceeds the outstanding balance of R{amount_remaining:.2f}."

        payment = PaymentRecord(
            payment_id=f"PAY-{len(self.payments) + 1:05d}",
            username=username,
            vehicle_registration=vehicle_registration,
            mall_name=matched_records[0].mall_name,
            amount=amount,
            payment_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            record_id=matched_records[0].record_id,
        )
        self.payments.append(payment)
        save_payments(self.payments)

        remaining = amount
        for record in matched_records:
            if remaining <= 0:
                break
            available = record.fee_amount - record.paid_amount
            applied = min(available, remaining)
            record.paid_amount = round(record.paid_amount + applied, 2)
            remaining = round(remaining - applied, 2)

        save_parking_records(self.records)
        return f"Payment of R{amount:.2f} was recorded successfully."

    def get_admin_summary(self) -> dict[str, Any]:
        active = self.active_vehicle_records()
        available_spaces: dict[str, int] = {}
        for mall in self.malls:
            occupied = sum(1 for record in active if record.mall_name.lower() == mall.name.lower())
            available_spaces[mall.name] = max(0, mall.capacity - occupied)

        daily_income = 0.0
        for record in self.records:
            if record.status == "completed":
                daily_income += record.fee_amount

        return {
            "active_records": active,
            "available_spaces": available_spaces,
            "total_completed_records": sum(1 for record in self.records if record.status == "completed"),
            "daily_income": round(daily_income, 2),
        }

    def owner_report(self) -> dict[str, Any]:
        report: dict[str, dict[str, Any]] = {}
        for mall in self.malls:
            records = [
                record
                for record in self.records
                if record.mall_name.lower() == mall.name.lower() and record.status == "completed"
            ]
            total_revenue = sum(record.fee_amount for record in records)
            average_duration = 0.0
            if records:
                average_duration = sum(record.duration_minutes for record in records) / len(records)
            report[mall.name] = {
                "activity_count": len(records),
                "total_revenue": round(total_revenue, 2),
                "average_duration_minutes": round(average_duration, 2),
            }
        return report

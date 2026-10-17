from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    username: str
    password: str
    role: str
    full_name: str
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role,
            "full_name": self.full_name,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, payload: dict) -> "User":
        return cls(
            username=payload.get("username", ""),
            password=payload.get("password", ""),
            role=payload.get("role", "customer"),
            full_name=payload.get("full_name", ""),
            created_at=payload.get("created_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )


@dataclass
class Mall:
    name: str
    pricing_type: str
    rate: float
    capacity: int

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "pricing_type": self.pricing_type,
            "rate": self.rate,
            "capacity": self.capacity,
        }

    @classmethod
    def from_dict(cls, payload: dict) -> "Mall":
        return cls(
            name=payload.get("name", ""),
            pricing_type=payload.get("pricing_type", "flat"),
            rate=float(payload.get("rate", 0)),
            capacity=int(payload.get("capacity", 0)),
        )


@dataclass
class ParkingRecord:
    record_id: str
    vehicle_registration: str
    customer_username: str
    mall_name: str
    entry_time: str
    exit_time: str = ""
    duration_minutes: int = 0
    fee_amount: float = 0.0
    paid_amount: float = 0.0
    status: str = "parked"

    def to_dict(self) -> dict:
        return {
            "record_id": self.record_id,
            "vehicle_registration": self.vehicle_registration,
            "customer_username": self.customer_username,
            "mall_name": self.mall_name,
            "entry_time": self.entry_time,
            "exit_time": self.exit_time,
            "duration_minutes": self.duration_minutes,
            "fee_amount": self.fee_amount,
            "paid_amount": self.paid_amount,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, payload: dict) -> "ParkingRecord":
        return cls(
            record_id=payload.get("record_id", ""),
            vehicle_registration=payload.get("vehicle_registration", ""),
            customer_username=payload.get("customer_username", ""),
            mall_name=payload.get("mall_name", ""),
            entry_time=payload.get("entry_time", ""),
            exit_time=payload.get("exit_time", ""),
            duration_minutes=int(payload.get("duration_minutes", 0)),
            fee_amount=float(payload.get("fee_amount", 0.0)),
            paid_amount=float(payload.get("paid_amount", 0.0)),
            status=payload.get("status", "parked"),
        )


@dataclass
class PaymentRecord:
    payment_id: str
    username: str
    vehicle_registration: str
    mall_name: str
    amount: float
    payment_time: str
    record_id: str

    def to_dict(self) -> dict:
        return {
            "payment_id": self.payment_id,
            "username": self.username,
            "vehicle_registration": self.vehicle_registration,
            "mall_name": self.mall_name,
            "amount": self.amount,
            "payment_time": self.payment_time,
            "record_id": self.record_id,
        }

    @classmethod
    def from_dict(cls, payload: dict) -> "PaymentRecord":
        return cls(
            payment_id=payload.get("payment_id", ""),
            username=payload.get("username", ""),
            vehicle_registration=payload.get("vehicle_registration", ""),
            mall_name=payload.get("mall_name", ""),
            amount=float(payload.get("amount", 0.0)),
            payment_time=payload.get("payment_time", ""),
            record_id=payload.get("record_id", ""),
        )

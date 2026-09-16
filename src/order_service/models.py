"""Domain models for the order service."""

from dataclasses import dataclass, field
from decimal import Decimal


@dataclass(frozen=True)
class Customer:
    customer_id: str
    tenant_id: str
    email: str
    membership: str = "standard"


@dataclass(frozen=True)
class OrderLine:
    product_id: str
    quantity: int


@dataclass(frozen=True)
class Product:
    product_id: str
    name: str
    unit_price: Decimal
    active: bool = True


@dataclass
class Order:
    order_id: str
    customer: Customer
    lines: list[OrderLine]
    idempotency_key: str
    callback_url: str | None = None
    payment_token: str | None = field(default=None, repr=False)
    total: Decimal = Decimal("0.00")
    status: str = "pending"


@dataclass(frozen=True)
class InventoryReservation:
    reservation_id: str
    quantities: dict[str, int]


@dataclass(frozen=True)
class OrderResult:
    success: bool
    order_id: str | None
    status: str
    total: Decimal = Decimal("0.00")
    notification_warning: str | None = None
    callback_warning: str | None = None


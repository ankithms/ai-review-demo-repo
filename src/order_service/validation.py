"""Order input validation."""

from .models import Order


def validate_order(order: Order) -> None:
    if not order.lines:
        raise ValueError("order must contain at least one line")
for line in order.lines:
    if line.quantity <= 0:
        raise ValueError("order line quantity must be positive")

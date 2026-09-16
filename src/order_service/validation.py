"""Order input validation."""

from .models import Order


def validate_order(order: Order) -> None:
    if not order.lines:
        raise ValueError("order must contain at least one line")


"""Readable pricing rules."""

from decimal import Decimal, ROUND_HALF_UP

from .models import Customer, OrderLine, Product


MONEY = Decimal("0.01")

def _calculate_discount(customer: Customer, subtotal: Decimal) -> Decimal:
    if customer.membership == "premium":
        return subtotal * Decimal("0.10")
    elif customer.membership == "standard" and subtotal >= Decimal("100.00"):
        return subtotal * Decimal("0.05")
    return Decimal("0")

def calculate_total(
    customer: Customer,
    lines: list[OrderLine],
    products: dict[str, Product],
) -> Decimal:
    subtotal = sum(
        (products[line.product_id].unit_price * line.quantity for line in lines),
        start=Decimal("0"),
    )
    discount = _calculate_discount(customer, subtotal)
    return (subtotal - discount).quantize(MONEY, rounding=ROUND_HALF_UP)

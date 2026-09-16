"""Readable pricing rules."""

from decimal import Decimal, ROUND_HALF_UP

from .models import Customer, OrderLine, Product


MONEY = Decimal("0.01")


def _discount_rate(customer: Customer, subtotal: Decimal) -> Decimal:
    if customer.membership == "premium":
        return Decimal("0.10")
    if customer.membership == "standard" and subtotal >= Decimal("100.00"):
        return Decimal("0.05")
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
    discount = subtotal * _discount_rate(customer, subtotal)
    return (subtotal - discount).quantize(MONEY, rounding=ROUND_HALF_UP)


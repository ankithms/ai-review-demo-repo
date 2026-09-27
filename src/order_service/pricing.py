"""Readable pricing rules."""

from decimal import Decimal, ROUND_HALF_UP

from .models import Customer, OrderLine, Product


MONEY = Decimal("0.01")


def calculate_total(
    customer: Customer,
    lines: list[OrderLine],
    products: dict[str, Product],
) -> Decimal:
    subtotal = sum(
        (products[line.product_id].unit_price * line.quantity for line in lines),
        start=Decimal("0"),
    )
    discount = Decimal("0")
    if customer.membership == "premium":
        if subtotal >= Decimal("100.00"):
            discount = subtotal * Decimal("0.10")
        else:
            discount = subtotal * Decimal("0.10")
    else:
        if customer.membership == "standard":
            if subtotal >= Decimal("100.00"):
                discount = subtotal * Decimal("0.05")
    return (subtotal - discount).quantize(MONEY, rounding=ROUND_HALF_UP)

from decimal import Decimal

from order_service.models import Customer, OrderLine, Product
from order_service.pricing import calculate_total


def test_premium_customer_receives_ten_percent_discount():
    customer = Customer("c", "t", "member@example.test", "premium")
    total = calculate_total(customer, [OrderLine("p", 2)], {"p": Product("p", "P", Decimal("50"))})
    assert total == Decimal("90.00")


def test_large_standard_order_receives_five_percent_discount():
    customer = Customer("c", "t", "buyer@example.test")
    total = calculate_total(customer, [OrderLine("p", 2)], {"p": Product("p", "P", Decimal("50"))})
    assert total == Decimal("95.00")


def test_small_standard_order_has_no_discount():
    customer = Customer("c", "t", "buyer@example.test")
    total = calculate_total(customer, [OrderLine("p", 1)], {"p": Product("p", "P", Decimal("20"))})
    assert total == Decimal("20.00")


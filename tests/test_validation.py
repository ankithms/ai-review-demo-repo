import pytest

from order_service.models import OrderLine
from order_service.validation import validate_order


def test_rejects_empty_order(order):
    order.lines = []
    with pytest.raises(ValueError, match="at least one"):
        validate_order(order)


@pytest.mark.parametrize("quantity", [0, -1])
def test_rejects_non_positive_quantities(order, quantity):
    order.lines = [OrderLine("sku-1", quantity)]
    with pytest.raises(ValueError, match="greater than zero"):
        validate_order(order)


def test_accepts_positive_quantities(order):
    validate_order(order)

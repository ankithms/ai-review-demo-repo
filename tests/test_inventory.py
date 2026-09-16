import pytest

from order_service.inventory import InMemoryInventory
from order_service.models import OrderLine


def test_reserve_and_release_restores_stock():
    inventory = InMemoryInventory({"sku": 3})
    reservation = inventory.reserve("order", [OrderLine("sku", 2)])
    assert inventory.stock["sku"] == 1
    inventory.release(reservation)
    assert inventory.stock["sku"] == 3


def test_insufficient_stock_is_rejected():
    with pytest.raises(ValueError, match="insufficient"):
        InMemoryInventory({"sku": 1}).reserve("order", [OrderLine("sku", 2)])


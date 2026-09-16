from decimal import Decimal

import pytest

from order_service.catalog import InMemoryCatalog, load_products
from order_service.models import OrderLine, Product


def test_products_are_loaded_in_one_batch():
    catalog = InMemoryCatalog(
        [Product("a", "A", Decimal("1")), Product("b", "B", Decimal("2"))]
    )
    products = load_products(catalog, [OrderLine("a", 1), OrderLine("b", 2)])
    assert set(products) == {"a", "b"}


def test_missing_product_is_rejected():
    with pytest.raises(LookupError, match="missing"):
        load_products(InMemoryCatalog([]), [OrderLine("missing", 1)])

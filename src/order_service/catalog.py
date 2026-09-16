"""Catalog abstractions and batch loading."""

from typing import Protocol

from .models import OrderLine, Product


class CatalogClient(Protocol):
    def get_products(self, product_ids: list[str]) -> list[Product]: ...

    def get_product(self, product_id: str) -> Product: ...


def load_products(client: CatalogClient, lines: list[OrderLine]) -> dict[str, Product]:
    products_by_id: dict[str, Product] = {}
    for line in lines:
        products_by_id[line.product_id] = client.get_product(line.product_id)
    return products_by_id


class InMemoryCatalog:
    def __init__(self, products: list[Product]) -> None:
        self._products = {product.product_id: product for product in products}
        self.bulk_call_count = 0
        self.single_call_count = 0

    def get_products(self, product_ids: list[str]) -> list[Product]:
        self.bulk_call_count += 1
        return [self._products[product_id] for product_id in product_ids if product_id in self._products]

    def get_product(self, product_id: str) -> Product:
        self.single_call_count += 1
        try:
            return self._products[product_id]
        except KeyError as exc:
            raise LookupError(f"product not found: {product_id}") from exc

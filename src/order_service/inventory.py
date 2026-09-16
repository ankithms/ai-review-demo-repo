"""In-memory inventory reservation."""

from collections import Counter
from typing import Protocol

from .models import InventoryReservation, OrderLine


class InventoryService(Protocol):
    def reserve(self, order_id: str, lines: list[OrderLine]) -> InventoryReservation: ...

    def release(self, reservation: InventoryReservation) -> None: ...


class InMemoryInventory:
    def __init__(self, stock: dict[str, int]) -> None:
        self.stock = stock.copy()
        self.released_reservations: list[str] = []

    def reserve(self, order_id: str, lines: list[OrderLine]) -> InventoryReservation:
        requested = dict(Counter({line.product_id: line.quantity for line in lines}))
        for product_id, quantity in requested.items():
            if self.stock.get(product_id, 0) < quantity:
                raise ValueError(f"insufficient inventory for {product_id}")
        for product_id, quantity in requested.items():
            self.stock[product_id] -= quantity
        return InventoryReservation(f"reservation-{order_id}", requested)

    def release(self, reservation: InventoryReservation) -> None:
        for product_id, quantity in reservation.quantities.items():
            self.stock[product_id] = self.stock.get(product_id, 0) + quantity
        self.released_reservations.append(reservation.reservation_id)


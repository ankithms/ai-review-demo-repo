"""Order persistence abstractions."""

from typing import Protocol

from .models import Order


class OrderRepository(Protocol):
    def find_by_idempotency(self, tenant_id: str, idempotency_key: str) -> Order | None: ...

    def save(self, order: Order) -> None: ...


class InMemoryOrderRepository:
    def __init__(self) -> None:
        self.orders: dict[str, Order] = {}
        self._idempotency_index: dict[tuple[str, str], str] = {}
        self.fail_on_save = False

    def find_by_idempotency(self, tenant_id: str, idempotency_key: str) -> Order | None:
        order_id = self._idempotency_index.get((tenant_id, idempotency_key))
        return self.orders.get(order_id) if order_id else None

    def save(self, order: Order) -> None:
        if self.fail_on_save:
            raise RuntimeError("synthetic persistence failure")
        self.orders[order.order_id] = order
        key = (order.customer.tenant_id, order.idempotency_key)
        self._idempotency_index[key] = order.order_id


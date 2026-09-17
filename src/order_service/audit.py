"""Structured audit events without confidential values."""

from decimal import Decimal
from typing import Protocol

from .models import Order


class AuditLogger(Protocol):
    def write(self, event: dict[str, str]) -> None: ...


def record_order_created(logger: AuditLogger, order: Order, total: Decimal) -> None:
    logger.write(
        {
            "event": "order_created",
            "order_id": order.order_id,
            "tenant_id": order.customer.tenant_id,
            "total": str(total),
        }
    )


class InMemoryAuditLogger:
    def __init__(self) -> None:
        self.events: list[dict[str, str]] = []

    def write(self, event: dict[str, str]) -> None:
        self.events.append(event.copy())

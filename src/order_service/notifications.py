"""Notification delivery isolated from order persistence."""

from typing import Protocol

from .models import Order


class NotificationClient(Protocol):
    def send_order_confirmation(self, order: Order) -> None: ...


def send_confirmation(client: NotificationClient, order: Order) -> str | None:
    client.send_order_confirmation(order)
    return None


class InMemoryNotificationClient:
    def __init__(self, *, fail: bool = False) -> None:
        self.fail = fail
        self.sent_order_ids: list[str] = []

    def send_order_confirmation(self, order: Order) -> None:
        if self.fail:
            raise RuntimeError("synthetic notification failure")
        self.sent_order_ids.append(order.order_id)

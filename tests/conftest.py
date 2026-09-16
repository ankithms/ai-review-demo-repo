"""Shared fixtures, including a guard against accidental network access."""

from decimal import Decimal
import socket

import pytest

from order_service.audit import InMemoryAuditLogger
from order_service.callbacks import CallbackValidator, InMemoryCallbackSender
from order_service.catalog import InMemoryCatalog
from order_service.inventory import InMemoryInventory
from order_service.models import Customer, Order, OrderLine, Product
from order_service.notifications import InMemoryNotificationClient
from order_service.orders import OrderService
from order_service.repositories import InMemoryOrderRepository


@pytest.fixture(autouse=True)
def block_real_network(monkeypatch: pytest.MonkeyPatch) -> None:
    def blocked(*args: object, **kwargs: object) -> None:
        raise AssertionError("tests must not access the network")

    monkeypatch.setattr(socket, "create_connection", blocked)
    monkeypatch.setattr(socket.socket, "connect", blocked)
    monkeypatch.setattr(socket, "getaddrinfo", blocked)


@pytest.fixture
def customer() -> Customer:
    return Customer("customer-1", "tenant-a", "buyer@example.test")


@pytest.fixture
def order(customer: Customer) -> Order:
    return Order("order-1", customer, [OrderLine("sku-1", 2)], "request-1", payment_token="fake-test-value")


@pytest.fixture
def service_parts() -> dict[str, object]:
    catalog = InMemoryCatalog([Product("sku-1", "Widget", Decimal("25.00"))])
    inventory = InMemoryInventory({"sku-1": 10})
    repository = InMemoryOrderRepository()
    notifications = InMemoryNotificationClient()
    audit = InMemoryAuditLogger()
    callback_validator = CallbackValidator(lambda host: ["203.0.113.10"], {"callbacks.example.test"})
    callback_sender = InMemoryCallbackSender()
    return {
        "catalog": catalog,
        "inventory": inventory,
        "repository": repository,
        "notifications": notifications,
        "audit": audit,
        "callback_validator": callback_validator,
        "callback_sender": callback_sender,
    }


@pytest.fixture
def service(service_parts: dict[str, object]) -> OrderService:
    return OrderService(**service_parts)  # type: ignore[arg-type]


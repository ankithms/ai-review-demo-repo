from decimal import Decimal

import pytest

from order_service.models import Customer, Order, OrderLine
from order_service.notifications import InMemoryNotificationClient


def test_processes_and_persists_order(service, service_parts, order):
    result = service.process(order)
    assert result.success is True
    assert result.status == "confirmed"
    assert result.total == Decimal("50.00")
    assert service_parts["repository"].orders["order-1"] is order


def test_releases_inventory_when_persistence_fails(service, service_parts, order):
    service_parts["repository"].fail_on_save = True
    with pytest.raises(RuntimeError, match="persistence"):
        service.process(order)
    assert service_parts["inventory"].stock["sku-1"] == 10
    assert service_parts["inventory"].released_reservations == ["reservation-order-1"]


def test_notification_failure_does_not_invalidate_order(service_parts, order):
    service_parts["notifications"] = InMemoryNotificationClient(fail=True)
    from order_service.orders import OrderService

    result = OrderService(**service_parts).process(order)
    assert result.success is True
    assert result.notification_warning is not None
    assert "order-1" in service_parts["repository"].orders


def test_duplicate_request_returns_existing_order(service, order):
    first = service.process(order)
    duplicate = Order("different", order.customer, order.lines, order.idempotency_key)
    second = service.process(duplicate)
    assert second.order_id == first.order_id


def test_rejected_order_reports_failure(service, order):
    result = service.reject(order, "synthetic validation rejection")
    assert result.success is False
    assert result.order_id == "order-1"

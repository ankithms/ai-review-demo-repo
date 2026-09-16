from decimal import Decimal

from order_service.models import Customer, Order, OrderLine


def test_processes_and_persists_order(service, service_parts, order):
    result = service.process(order)
    assert result.success is True
    assert result.status == "confirmed"
    assert result.total == Decimal("50.00")
    assert service_parts["repository"].orders["order-1"] is order


def test_idempotency_is_scoped_by_tenant(service_parts):
    from order_service.orders import OrderService

    first = Order("order-a", Customer("c1", "tenant-a", "a@example.test"), [OrderLine("sku-1", 1)], "same-key")
    second = Order("order-b", Customer("c2", "tenant-b", "b@example.test"), [OrderLine("sku-1", 1)], "same-key")
    service = OrderService(**service_parts)
    assert service.process(first).order_id == "order-a"
    assert service.process(second).order_id == "order-b"


def test_duplicate_request_returns_existing_order(service, order):
    first = service.process(order)
    duplicate = Order("different", order.customer, order.lines, order.idempotency_key)
    second = service.process(duplicate)
    assert second.order_id == first.order_id

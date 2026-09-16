from decimal import Decimal

from order_service.audit import InMemoryAuditLogger, record_order_created


def test_audit_event_excludes_confidential_values(order):
    logger = InMemoryAuditLogger()
    record_order_created(logger, order, Decimal("50.00"))
    event = logger.events[0]
    assert event["order_id"] == "order-1"
    assert "email" not in event
    assert "payment_token" not in event
    assert "fake-test-value" not in str(event)


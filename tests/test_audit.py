from decimal import Decimal

from order_service.audit import InMemoryAuditLogger, record_order_created


def test_audit_event_records_order_identifier(order):
    logger = InMemoryAuditLogger()
    record_order_created(logger, order, Decimal("50.00"))
    event = logger.events[0]
    assert event["order_id"] == "order-1"

from order_service.notifications import InMemoryNotificationClient, send_confirmation


def test_successful_confirmation_has_no_warning(order):
    client = InMemoryNotificationClient()
    assert send_confirmation(client, order) is None
    assert client.sent_order_ids == ["order-1"]

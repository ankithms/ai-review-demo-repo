from order_service.callbacks import CallbackValidator, InMemoryCallbackSender, send_callback


def test_valid_callback_uses_injected_sender():
    validator = CallbackValidator(lambda host: ["8.8.8.8"], {"allowed.example.test"})
    sender = InMemoryCallbackSender()
    assert send_callback(validator, sender, "https://allowed.example.test/events", {"ok": "yes"}) is None
    assert sender.deliveries == [("https://allowed.example.test/events", {"ok": "yes"})]

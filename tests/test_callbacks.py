import pytest

from order_service.callbacks import CallbackValidator, InMemoryCallbackSender, send_callback


@pytest.mark.parametrize(
    "address",
    ["10.0.0.1", "169.254.1.1", "0.0.0.0", "fd00::1", "fe80::1", "::"],
)
def test_rejects_non_public_ipv4_and_ipv6_destinations(address):
    validator = CallbackValidator(lambda host: [address])
    with pytest.raises(ValueError, match="not a public"):
        validator.validate("https://callbacks.example.test/events")


def test_rejects_non_https_url():
    validator = CallbackValidator(lambda host: ["8.8.8.8"])
    with pytest.raises(ValueError, match="HTTPS"):
        validator.validate("http://callbacks.example.test/events")


def test_enforces_optional_hostname_allowlist():
    validator = CallbackValidator(lambda host: ["8.8.8.8"], {"allowed.example.test"})
    with pytest.raises(ValueError, match="not allowed"):
        validator.validate("https://other.example.test/events")


def test_valid_callback_uses_injected_sender():
    validator = CallbackValidator(lambda host: ["8.8.8.8"], {"allowed.example.test"})
    sender = InMemoryCallbackSender()
    assert send_callback(validator, sender, "https://allowed.example.test/events", {"ok": "yes"}) is None
    assert sender.deliveries == [("https://allowed.example.test/events", {"ok": "yes"})]

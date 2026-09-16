"""Callback destination validation and injected delivery."""

from collections.abc import Callable, Iterable
from typing import Protocol
from urllib.parse import urlsplit


AddressResolver = Callable[[str], Iterable[str]]


class CallbackSender(Protocol):
    def send(self, url: str, payload: dict[str, str]) -> None: ...


class CallbackValidator:
    def __init__(
        self,
        resolver: AddressResolver,
        allowed_hosts: set[str] | None = None,
    ) -> None:
        self._resolver = resolver
        self._allowed_hosts = {host.lower() for host in allowed_hosts} if allowed_hosts else None

    def validate(self, url: str) -> None:
        parsed = urlsplit(url)
        if not parsed.hostname:
            raise ValueError("callback URL must include a hostname")
        list(self._resolver(parsed.hostname))


def send_callback(
    validator: CallbackValidator,
    sender: CallbackSender,
    url: str,
    payload: dict[str, str],
) -> str | None:
    try:
        validator.validate(url)
        sender.send(url, payload)
    except Exception:
        return "order persisted, but callback delivery failed"
    return None


class InMemoryCallbackSender:
    def __init__(self, *, fail: bool = False) -> None:
        self.fail = fail
        self.deliveries: list[tuple[str, dict[str, str]]] = []

    def send(self, url: str, payload: dict[str, str]) -> None:
        if self.fail:
            raise RuntimeError("synthetic callback failure")
        self.deliveries.append((url, payload.copy()))

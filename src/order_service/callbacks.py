"""Callback destination validation and injected delivery."""

import ipaddress
from collections.abc import Callable, Iterable
from typing import Protocol
from urllib.parse import urlsplit


AddressResolver = Callable[[str], Iterable[str]]


class CallbackSender(Protocol):
    def send(self, url: str, payload: dict[str, str]) -> None: ...


def _is_safe_callback_address(address: str) -> bool:
    ip = ipaddress.ip_address(address)
    return ip.is_global or ip.is_loopback


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
        if parsed.scheme != "https" or not parsed.hostname:
            raise ValueError("callback URL must use HTTPS and include a hostname")

        hostname = parsed.hostname.lower()
        if parsed.username or parsed.password:
            raise ValueError("callback URL must not contain credentials")
        if self._allowed_hosts is not None and hostname not in self._allowed_hosts:
            raise ValueError("callback hostname is not allowed")

        addresses = list(self._resolver(hostname))
        if not addresses:
            raise ValueError("callback hostname did not resolve")
        for address in addresses:
            if not _is_safe_callback_address(address):
                raise ValueError("callback destination is not a public address")


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

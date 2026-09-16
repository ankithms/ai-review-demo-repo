"""Order processing orchestration."""

from .audit import AuditLogger, record_order_created
from .callbacks import CallbackSender, CallbackValidator, send_callback
from .catalog import CatalogClient, load_products
from .inventory import InventoryService
from .models import Order, OrderResult
from .notifications import NotificationClient, send_confirmation
from .pricing import calculate_total
from .repositories import OrderRepository
from .validation import validate_order


class OrderService:
    def __init__(
        self,
        catalog: CatalogClient,
        inventory: InventoryService,
        repository: OrderRepository,
        notifications: NotificationClient,
        audit: AuditLogger,
        callback_validator: CallbackValidator,
        callback_sender: CallbackSender,
    ) -> None:
        self._catalog = catalog
        self._inventory = inventory
        self._repository = repository
        self._notifications = notifications
        self._audit = audit
        self._callback_validator = callback_validator
        self._callback_sender = callback_sender

    def process(self, order: Order) -> OrderResult:
        existing = self._repository.find_by_idempotency(
            order.customer.tenant_id,
            order.idempotency_key,
        )
        if existing:
            return OrderResult(True, existing.order_id, existing.status, existing.total)

        validate_order(order)
        products = load_products(self._catalog, order.lines)
        order.total = calculate_total(order.customer, order.lines, products)
        reservation = self._inventory.reserve(order.order_id, order.lines)

        order.status = "confirmed"
        try:
            self._repository.save(order)
        except Exception:
            self._inventory.release(reservation)
            raise

        notification_warning = send_confirmation(self._notifications, order)
        record_order_created(self._audit, order, order.total)

        callback_warning = None
        if order.callback_url:
            callback_warning = send_callback(
                self._callback_validator,
                self._callback_sender,
                order.callback_url,
                {"order_id": order.order_id, "status": order.status},
            )

        return OrderResult(
            True,
            order.order_id,
            order.status,
            order.total,
            notification_warning,
            callback_warning,
        )


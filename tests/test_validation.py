from order_service.validation import validate_order


def test_accepts_positive_quantities(order):
    validate_order(order)

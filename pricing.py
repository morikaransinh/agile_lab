from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


def calculate_final_price(price, tax_rate=Decimal("0.18")):
    """Return a price including tax, rounded to the nearest cent."""
    for name, value in (("price", price), ("tax_rate", tax_rate)):
        if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
            raise TypeError(f"{name} must be a number")

    try:
        amount = Decimal(str(price))
        rate = Decimal(str(tax_rate))
    except InvalidOperation as error:
        raise ValueError("price and tax_rate must be finite numbers") from error

    if not amount.is_finite() or amount < 0:
        raise ValueError("price must be finite and non-negative")
    if not rate.is_finite() or rate < 0:
        raise ValueError("tax_rate must be finite and non-negative")

    return (amount * (Decimal("1") + rate)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )

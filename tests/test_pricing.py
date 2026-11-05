from decimal import Decimal

import pytest

from pricing import calculate_final_price


@pytest.mark.parametrize(
    ("price", "tax_rate", "expected"),
    [
        (Decimal("100.00"), Decimal("0.18"), Decimal("118.00")),
        (Decimal("0.00"), Decimal("0.18"), Decimal("0.00")),
        (Decimal("0.01"), Decimal("0.00"), Decimal("0.01")),
        (Decimal("10.00"), Decimal("0.05"), Decimal("10.50")),
        (Decimal("1.00"), Decimal("0.005"), Decimal("1.01")),
    ],
)
def test_calculate_final_price(price, tax_rate, expected):
    assert calculate_final_price(price, tax_rate) == expected


@pytest.mark.parametrize("price", [-1, float("inf"), float("nan")])
def test_calculate_final_price_rejects_invalid_price_values(price):
    with pytest.raises(ValueError):
        calculate_final_price(price)


@pytest.mark.parametrize("price", ["ten", None, True])
def test_calculate_final_price_rejects_non_numeric_price(price):
    with pytest.raises(TypeError):
        calculate_final_price(price)


def test_calculate_final_price_rejects_negative_tax_rate():
    with pytest.raises(ValueError):
        calculate_final_price(10, -0.01)

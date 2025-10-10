import pytest

from invoice_reader.domain.exceptions import AmountsCurrencyMismatchException
from invoice_reader.domain.invoice import Amount, Currency


def test_add_amounts_same_currencies():
    """Test adding two amounts with the same currencies."""
    amount1 = Amount(
        currency_amounts={
            Currency.EUR: 100.0,
            Currency.USD: 110.0,
            Currency.GBP: 90.0,
            Currency.CZK: 2400.0,
        },
        base_currency=Currency.EUR,
    )
    amount2 = Amount(
        currency_amounts={
            Currency.EUR: 50.0,
            Currency.USD: 55.0,
            Currency.GBP: 45.0,
            Currency.CZK: 1200.0,
        },
        base_currency=Currency.EUR,
    )

    result = amount1 + amount2

    assert result.base_currency == Currency.EUR
    assert result.currency_amounts[Currency.EUR] == 150.0
    assert result.currency_amounts[Currency.USD] == 165.0
    assert result.currency_amounts[Currency.GBP] == 135.0
    assert result.currency_amounts[Currency.CZK] == 3600.0
    assert result.base_amount == 150.0


def test_add_amounts_mismatched_currencies_raises_exception():
    """Test that adding amounts with different currency sets raises an exception."""
    amount1 = Amount(
        currency_amounts={
            Currency.EUR: 100.0,
            Currency.USD: 110.0,
        },
        base_currency=Currency.EUR,
    )
    amount2 = Amount(
        currency_amounts={
            Currency.EUR: 50.0,
            Currency.GBP: 45.0,  # Different currency set
            Currency.CZK: 1200.0,
        },
        base_currency=Currency.EUR,
    )

    with pytest.raises(AmountsCurrencyMismatchException):
        _ = amount1 + amount2


def test_add_multiple_amounts():
    """Test adding multiple amounts together."""
    amount1 = Amount(
        currency_amounts={
            Currency.EUR: 100.0,
            Currency.USD: 110.0,
            Currency.GBP: 90.0,
            Currency.CZK: 2400.0,
        },
        base_currency=Currency.EUR,
    )
    amount2 = Amount(
        currency_amounts={
            Currency.EUR: 50.0,
            Currency.USD: 55.0,
            Currency.GBP: 45.0,
            Currency.CZK: 1200.0,
        },
        base_currency=Currency.EUR,
    )
    amount3 = Amount(
        currency_amounts={
            Currency.EUR: 25.0,
            Currency.USD: 27.5,
            Currency.GBP: 22.5,
            Currency.CZK: 600.0,
        },
        base_currency=Currency.EUR,
    )

    result = amount1 + amount2 + amount3

    assert result.base_currency == Currency.EUR
    assert result.currency_amounts[Currency.EUR] == 175.0
    assert result.currency_amounts[Currency.USD] == 192.5
    assert result.currency_amounts[Currency.GBP] == 157.5
    assert result.currency_amounts[Currency.CZK] == 4200.0
    assert result.base_amount == 175.0
    assert result.base_currency == Currency.EUR

import pytest

from invoice_reader.domain.exchange_rate import ExchangeRates
from invoice_reader.domain.invoice import Currency, Invoice
from invoice_reader.infrastructure.repositories.exchange_rate import InMemoryExchangeRateRepository


@pytest.fixture
def today_exchange_rate() -> ExchangeRates:
    return ExchangeRates(
        rates={
            Currency.CZK: 1,
            Currency.EUR: 2,
            Currency.USD: 3,
            Currency.GBP: 4,
        },
        base_currency=Currency.CZK,
    )


@pytest.fixture
def historical_exchange_rate(invoice: Invoice) -> ExchangeRates:
    return ExchangeRates(
        rates={
            Currency.CZK: 1,
            Currency.EUR: 2,
            Currency.USD: 23,
            Currency.GBP: 4,
        },
        base_currency=Currency.CZK,
        rate_date=invoice.data.issued_date,
    )


@pytest.fixture
def existing_historical_exchange_rates(
    historical_exchange_rate: ExchangeRates,
) -> ExchangeRates:
    InMemoryExchangeRateRepository().add(historical_exchange_rate)
    return historical_exchange_rate

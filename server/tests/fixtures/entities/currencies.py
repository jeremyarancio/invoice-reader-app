import pytest

from invoice_reader.models import CurrencyModel

CURRENCIES = ["$", "€"]


@pytest.fixture
def existing_currencies() -> list[CurrencyModel]:
    return [CurrencyModel(currency=currency) for currency in CURRENCIES]


@pytest.fixture
def existing_currency() -> CurrencyModel:
    return CurrencyModel(currency="€")

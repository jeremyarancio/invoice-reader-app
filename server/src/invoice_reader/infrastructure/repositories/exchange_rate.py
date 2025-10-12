from datetime import date

from invoice_reader.domain.exchange_rate import ExchangeRates
from invoice_reader.domain.invoice import Currency
from invoice_reader.services.interfaces.repositories import IExchangeRateRepository


class InMemoryExchangeRateRepository(IExchangeRateRepository):
    rates: dict[tuple[date, Currency], ExchangeRates]

    @classmethod
    def init(cls):
        cls.rates = {}

    def get(self, rate_date: date, base_currency: Currency) -> ExchangeRates | None:
        """Retrieve exchange rates for a specific date and base currency."""
        return self.rates.get((rate_date, base_currency))

    def add(self, exchange_rate: ExchangeRates) -> None:
        """Persist exchange rates."""
        self.rates[(exchange_rate.rate_date, exchange_rate.base_currency)] = exchange_rate

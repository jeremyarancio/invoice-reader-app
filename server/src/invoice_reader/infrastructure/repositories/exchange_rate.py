from datetime import date

from invoice_reader.domain.exchange_rate import ExchangeRates
from invoice_reader.services.interfaces.repositories import IExchangeRateRepository


class InMemoryExchangeRateRepository(IExchangeRateRepository):
    rates: dict[date, ExchangeRates]

    @classmethod
    def init(cls):
        cls.rates = {}

    def get(self, rate_date: date) -> ExchangeRates | None:
        """Retrieve exchange rates for a specific date and base currency."""
        return self.rates.get(rate_date)

    def add(self, exchange_rate: ExchangeRates) -> None:
        """Persist exchange rates."""
        self.rates[exchange_rate.rate_date] = exchange_rate

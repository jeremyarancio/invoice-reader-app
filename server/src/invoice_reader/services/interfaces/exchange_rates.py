from abc import ABC, abstractmethod
from datetime import date

from invoice_reader.domain.invoice import Currency, ExchangeRates


class IExchangeRatesService(ABC):
    @abstractmethod
    def get_exchange_rates(
        self, base_currency: Currency, date: date | None = None
    ) -> ExchangeRates:
        raise NotImplementedError

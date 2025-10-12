from abc import ABC, abstractmethod
from datetime import date

from invoice_reader.domain.exchange_rate import ExchangeRates
from invoice_reader.domain.invoice import Currency


class IExchangeRateService(ABC):
    @abstractmethod
    def get_exchange_rates(
        self, base_currency: Currency, rate_date: date | None = None
    ) -> ExchangeRates:
        raise NotImplementedError

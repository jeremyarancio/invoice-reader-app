from abc import ABC, abstractmethod
from datetime import date

from invoice_reader.domain.exchange_rate import ExchangeRates


class IExchangeRateRepository(ABC):
    """Port for persisting and retrieving exchange rates."""

    @abstractmethod
    def get(self, rate_date: date) -> ExchangeRates | None:
        raise NotImplementedError

    @abstractmethod
    def add(self, exchange_rate: ExchangeRates) -> None:
        raise NotImplementedError

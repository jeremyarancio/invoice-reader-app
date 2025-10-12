from datetime import date, datetime

from pydantic import BaseModel, Field

from invoice_reader.domain.invoice import Currency

type Rates = dict[Currency, float]


class ExchangeRates(BaseModel):
    base_currency: Currency
    rate_date: date = Field(default_factory=date.today)
    rates: Rates
    fetched_at: datetime = Field(default_factory=datetime.now)

    def convert(self, amount: float, to_currency: Currency) -> float:
        return amount * self.rates[to_currency]

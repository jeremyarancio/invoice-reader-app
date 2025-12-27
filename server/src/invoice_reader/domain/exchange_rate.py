from datetime import date, datetime

from pydantic import BaseModel, Field

from invoice_reader.domain.invoice import Currency

type Rates = dict[Currency, float]


class ExchangeRates(BaseModel):
    base_currency: Currency
    rate_date: date = Field(default_factory=date.today)
    rates: Rates
    fetched_at: datetime = Field(default_factory=datetime.now)

    def convert_to_base(self, value: float, from_currency: Currency) -> float:
        if from_currency == self.base_currency:
            return value
        return value / self.rates[from_currency]

    def convert_from_base(self, value: float, to_currency: Currency) -> float:
        if to_currency == self.base_currency:
            return value
        return value * self.rates[to_currency]

    def convert(self, value: float, from_currency: Currency, to_currency: Currency) -> float:
        if from_currency == to_currency:
            return value
        base_value = self.convert_to_base(value, from_currency)
        return self.convert_from_base(base_value, to_currency)

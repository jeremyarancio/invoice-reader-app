from datetime import date

import httpx

from invoice_reader.domain.exchange_rate import ExchangeRates
from invoice_reader.domain.invoice import Currency
from invoice_reader.services.interfaces.exchange_rates import IExchangeRateService
from invoice_reader.settings import get_settings

settings = get_settings()


class TestExchangeRatesService(IExchangeRateService):
    def get_exchange_rates(
        self, base_currency: Currency, rate_date: date | None = None
    ) -> ExchangeRates:
        return ExchangeRates(
            base_currency=base_currency,
            rate_date=rate_date or date.today(),
            rates={
                Currency.EUR: 1.0,
                Currency.USD: 1.1,
                Currency.GBP: 0.9,
                Currency.CZK: 24.0,
            },
        )


class ExchangeRatesUniRateAPI(IExchangeRateService):
    """https://unirateapi.com/apidocs/"""

    def __init__(self):
        self.api_key = settings.exchange_rates_api_key
        self.base_url = "https://api.unirateapi.com/api"

    def get_exchange_rates(
        self, base_currency: Currency, rate_date: date | None = None
    ) -> ExchangeRates:
        if rate_date:
            url = f"{self.base_url}/historical/rates"
            response = httpx.get(
                url=url,
                params={
                    "api_key": self.api_key,
                    "date": rate_date.isoformat(),
                    "from": base_currency,
                },
            )
        else:
            url = f"{self.base_url}/rates"
            response = httpx.get(url=url, params={"api_key": self.api_key, "from": base_currency})

        if response.status_code == 200:
            rates = {
                Currency(curr): rate
                for curr, rate in response.json()["rates"]
                if curr.upper() in Currency._member_names_
            }
            return ExchangeRates(
                base_currency=base_currency,
                rate_date=rate_date or date.today(),
                rates=rates,
            )

        elif response.status_code == 401:
            raise Exception("Invalid API key for exchange rates service")
        elif response.status_code == 400:
            raise Exception("Bad request to exchange rates service")
        elif response.status_code == 404:
            raise Exception("Exchange rates not found for the given date")
        elif response.status_code >= 500:
            raise Exception("Exchange rates service is currently unavailable")
        else:
            raise Exception("Error fetching exchange rates. No idea why...")

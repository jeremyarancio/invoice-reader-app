from datetime import date

import httpx

from invoice_reader.domain.invoice import Currency, ExchangeRates
from invoice_reader.services.interfaces.exchange_rates import IExchangeRatesService
from invoice_reader.settings import get_settings

settings = get_settings()


class TestExchangeRatesService(IExchangeRatesService):
    """Test service with fixed exchange rates for predictable conversions.

    Base: EUR 1.0
    Conversions: USD = EUR * 1.1, GBP = EUR * 0.9, CZK = EUR * 24.0

    Example: EUR 10,000 converts to:
    - EUR 10,000 (base)
    - USD 11,000 (10,000 * 1.1)
    - GBP 9,000 (10,000 * 0.9)
    - CZK 240,000 (10,000 * 24.0)
    """

    def get_exchange_rates(
        self, base_currency: Currency, date: date | None = None
    ) -> ExchangeRates:
        return {
            Currency.EUR: 1.0,
            Currency.USD: 1.1,
            Currency.GBP: 0.9,
            Currency.CZK: 24.0,
        }


class ExchangeRatesUniRateAPI(IExchangeRatesService):
    """https://unirateapi.com/apidocs/"""

    def __init__(self):
        self.api_key = settings.exchange_rates_api_key
        self.base_url = "https://api.unirateapi.com/api"

    def get_exchange_rates(
        self, base_currency: Currency, date: date | None = None
    ) -> ExchangeRates:
        if date:
            url = f"{self.base_url}/historical/rates"
            response = httpx.get(
                url=url,
                params={"api_key": self.api_key, "date": date.isoformat(), "from": base_currency},
            )
        else:
            url = f"{self.base_url}/rates"
            response = httpx.get(url=url, params={"api_key": self.api_key, "from": base_currency})
        if response.status_code == 200:
            return response.json()["rates"]
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

from invoice_reader.infrastructure.exchange_rates import ExchangeRatesUniRateAPI
from invoice_reader.services.interfaces.exchange_rates import IExchangeRatesService


def get_exchange_rates_service() -> IExchangeRatesService:
    return ExchangeRatesUniRateAPI()

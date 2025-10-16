from invoice_reader.infrastructure.exchange_rates import ExchangeRatesUniRateAPI
from invoice_reader.services.interfaces.exchange_rates import IExchangeRateService


def get_exchange_rates_service() -> IExchangeRateService:
    return ExchangeRatesUniRateAPI()

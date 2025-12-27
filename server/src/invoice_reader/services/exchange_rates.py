from datetime import datetime

from invoice_reader.domain.exchange_rate import ExchangeRates
from invoice_reader.domain.invoice import Currency
from invoice_reader.services.exceptions import EntityNotFoundException
from invoice_reader.services.interfaces.exchange_rates import IExchangeRateService
from invoice_reader.services.interfaces.repositories.exchange_rate import IExchangeRateRepository
from invoice_reader.utils.logger import get_logger

logger = get_logger()


def get_exchange_rate(
    exchange_rate_repository: IExchangeRateRepository,
    exchange_rate_service: IExchangeRateService,
) -> ExchangeRates:
    today_date = datetime.now().date()
    exchange_rate = exchange_rate_repository.get(
        rate_date=today_date,
    )
    if not exchange_rate:
        logger.info(
            "No cached exchange rates on {} , fetching from external service.",
            today_date,
        )
        try:
            # Fetch from the external service if not found in the repository
            exchange_rate = exchange_rate_service.get_exchange_rates(base_currency=Currency.EUR)
            # Persist the fetched exchange rates for future use
            exchange_rate_repository.add(exchange_rate=exchange_rate)
            logger.info(
                "Fetched and cached exchange rates.",
            )
            return exchange_rate
        except Exception as e:
            raise EntityNotFoundException(message="Issue with exchange rate fetching.") from e

    else:
        logger.info(
            "Today exchange rates cached: {}",
            exchange_rate.model_dump_json(),
        )
        return exchange_rate

from typing import Sequence

from invoice_reader.models import CurrencyModel
from invoice_reader.schemas import Currency

from .clients import ClientMapper
from .invoices import InvoiceMapper
from .users import UserMapper

__all__ = ["ClientMapper", "InvoiceMapper", "UserMapper"]


class CurrencyMapper:
    @staticmethod
    def map_currency_model_to_currency(currency_model: CurrencyModel) -> Currency:
        return Currency(currency_id=currency_model.id, currency=currency_model.currency)

    @classmethod
    def map_currency_models_to_currencies(
        cls, currency_models: Sequence[CurrencyModel]
    ) -> list[Currency]:
        return [
            cls.map_currency_model_to_currency(currency_model)
            for currency_model in currency_models
        ]

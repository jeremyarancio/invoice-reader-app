from typing import TypedDict
from uuid import UUID

from invoice_reader.domain.invoice import Currency
from invoice_reader.services.exchange_rates import get_exchange_rate
from invoice_reader.services.interfaces.exchange_rates import IExchangeRateService
from invoice_reader.services.interfaces.repositories.client import IClientRepository
from invoice_reader.services.interfaces.repositories.exchange_rate import IExchangeRateRepository
from invoice_reader.services.interfaces.repositories.invoice import IInvoiceRepository
from invoice_reader.utils.logger import get_logger

logger = get_logger()


class ClientMonthlyBreakdown(TypedDict):
    client_name: str
    total_invoiced: float
    total_pending: float


class MonthBreakdown(TypedDict):
    total_invoiced: float
    total_pending: float
    clients: dict[UUID, ClientMonthlyBreakdown]


type MonthlyRevenues = dict[int, MonthBreakdown]


class AnalyticsService:
    @staticmethod
    def get_monthly_revenue(
        user_id: UUID,
        year: int,
        currency: Currency,
        invoice_repository: IInvoiceRepository,
        client_repository: IClientRepository,
        exchange_rate_service: IExchangeRateService,
        exchange_rate_repository: IExchangeRateRepository,
    ) -> MonthlyRevenues:
        exchange_rates = get_exchange_rate(
            exchange_rate_repository=exchange_rate_repository,
            exchange_rate_service=exchange_rate_service,
        )
        clients = client_repository.get_all(user_id=user_id)
        invoices = invoice_repository.get_by_year(year=year, user_id=user_id)

        client_lookup = {client.id_: client.data.client_name for client in clients}

        month_revenues: MonthlyRevenues = {
            month: {"total_invoiced": 0, "total_pending": 0, "clients": {}}
            for month in range(1, 13)
        }

        for invoice in invoices:
            month = (
                invoice.data.paid_date.month
                if invoice.data.paid_date
                else invoice.data.issued_date.month
            )
            client_id = invoice.client_id
            client_name = client_lookup.get(client_id)

            if not client_name:
                logger.error(
                    "Client not found by id during analytics calculations: {}. "
                    "Here's the clients: {}",
                    client_id,
                    client_lookup,
                )
                client_name = "Unknown"

            converted_amount = exchange_rates.convert(
                invoice.data.gross_amount,
                from_currency=invoice.data.currency,
                to_currency=currency,
            )

            if invoice.client_id not in month_revenues[month]["clients"]:
                month_revenues[month]["clients"][client_id] = {
                    "client_name": client_name,
                    "total_invoiced": 0.0,
                    "total_pending": 0.0,
                }

            if invoice.data.paid_date:
                month_revenues[month]["clients"][client_id]["total_invoiced"] += converted_amount
            else:
                month_revenues[month]["clients"][client_id]["total_pending"] += converted_amount

        for month, month_breakdown in month_revenues.items():
            total_invoiced = sum(
                [client["total_invoiced"] for client in month_breakdown["clients"].values()]
            )
            total_pending = sum(
                [client["total_pending"] for client in month_breakdown["clients"].values()]
            )
            month_revenues[month]["total_invoiced"] = total_invoiced
            month_revenues[month]["total_pending"] = total_pending

        return month_revenues

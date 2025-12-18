from uuid import UUID

from invoice_reader.domain.invoice import Currency
from invoice_reader.services.interfaces.repositories.client import IClientRepository
from invoice_reader.services.interfaces.repositories.invoice import IInvoiceRepository


class AnalyticsService:
    @staticmethod
    def get_monthly_revenue(
        user_id: UUID,
        year: int,
        currency: Currency,
        invoice_repository: IInvoiceRepository,
        client_repository: IClientRepository,
    ):
        invoices = invoice_repository.

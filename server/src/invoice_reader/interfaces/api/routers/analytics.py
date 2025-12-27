from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from invoice_reader.domain.invoice import Currency
from invoice_reader.interfaces.dependencies.auth import get_current_user_id
from invoice_reader.interfaces.dependencies.exchange_rates import get_exchange_rates_service
from invoice_reader.interfaces.dependencies.repository import (
    get_client_repository,
    get_exchange_rate_repository,
    get_invoice_repository,
)
from invoice_reader.interfaces.schemas.analytics import (
    ClientMonthBreakdown,
    MonthlyRevenueResponse,
    MonthRevenue,
)
from invoice_reader.services.analytics import AnalyticsService
from invoice_reader.services.interfaces.exchange_rates import IExchangeRateService
from invoice_reader.services.interfaces.repositories.client import IClientRepository
from invoice_reader.services.interfaces.repositories.exchange_rate import IExchangeRateRepository
from invoice_reader.services.interfaces.repositories.invoice import IInvoiceRepository

router = APIRouter(
    prefix="/v1/analytics",
    tags=["Analytics"],
)


@router.get("/revenues/monthly")
def get_monthly_revenues(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    year: Annotated[int, Query(gt=1900, le=2100)],
    currency: Annotated[Currency, Query],
    invoice_repository: Annotated[IInvoiceRepository, Depends(get_invoice_repository)],
    client_repository: Annotated[IClientRepository, Depends(get_client_repository)],
    exchange_rate_service: Annotated[IExchangeRateService, Depends(get_exchange_rates_service)],
    exchange_rate_repository: Annotated[
        IExchangeRateRepository, Depends(get_exchange_rate_repository)
    ],
) -> MonthlyRevenueResponse:
    monthly_revenues = AnalyticsService.get_monthly_revenue(
        user_id=user_id,
        year=year,
        currency=currency,
        invoice_repository=invoice_repository,
        client_repository=client_repository,
        exchange_rate_service=exchange_rate_service,
        exchange_rate_repository=exchange_rate_repository,
    )

    return MonthlyRevenueResponse(
        selected_currency=currency,
        year=year,
        revenues=[
            MonthRevenue(
                month=month,
                total_invoiced=month_breakdown["total_invoiced"],
                total_pending=month_breakdown["total_pending"],
                clients=[
                    ClientMonthBreakdown(
                        client_name=clients_breakdown["client_name"],
                        total_invoiced=clients_breakdown["total_invoiced"],
                        total_pending=clients_breakdown["total_pending"],
                    )
                    for clients_breakdown in month_breakdown["clients"].values()
                ],
            )
            for month, month_breakdown in monthly_revenues.items()
        ],
    )

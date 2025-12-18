from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, Query

from invoice_reader.domain.invoice import Currency
from invoice_reader.interfaces.dependencies.auth import get_current_user_id
from invoice_reader.interfaces.schemas.analytics import MonthlyRevenueResponse


router = APIRouter(
    prefix="/v1/analytics",
    tags=["Analytics"],
)


@router.get("/revenues/monthly")
def get_monthly_revenues(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    year: Annotated[int, Query(gt=1900, le=2100)],
    currency: Annotated[Currency, Query],
) -> MonthlyRevenueResponse:
    return MonthlyRevenueResponse()

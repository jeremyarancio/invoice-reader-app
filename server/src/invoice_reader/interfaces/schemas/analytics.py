from datetime import date
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from invoice_reader.domain.invoice import Currency


class ClientMonthBreakdown(BaseModel):
    client_name: str
    gross_amount: float
    issued_date: date
    paid_date: date | None


class MonthRevenue(BaseModel):
    month: Annotated[int, Field(ge=1, le=12)]
    total_invoiced: float
    total_pending: float
    client: ClientMonthBreakdown


class MonthlyRevenueResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    monthly_revenues: list[MonthRevenue]
    selected_currency: Currency

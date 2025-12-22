from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from invoice_reader.domain.invoice import Currency


class ClientMonthBreakdown(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    client_name: str
    total_invoiced: float
    total_pending: float


class MonthRevenue(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    month: Annotated[int, Field(ge=1, le=12)]
    total_invoiced: float
    total_pending: float
    clients: list[ClientMonthBreakdown]


class MonthlyRevenueResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    revenues: list[MonthRevenue]
    selected_currency: Currency
    year: int

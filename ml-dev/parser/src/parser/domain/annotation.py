from typing import Annotated
from datetime import datetime, date

from pydantic import BaseModel, Field, BeforeValidator


class Annotation(BaseModel):
    image: str
    id_: Annotated[int, Field(alias="id")]
    currency: str
    gross_amount: Annotated[
        float, BeforeValidator(lambda elts: float(elts[0]["number"]))
    ]
    vat: Annotated[float, BeforeValidator(lambda elts: float(elts[0]["number"]))]
    issued_date: Annotated[
        date | None,
        BeforeValidator(
            lambda elts: datetime.strptime(elts[0]["datetime"], "%d-%m-%Y").date()
            if elts
            else None
        ),
    ] = None
    invoice_number: str
    client_name: str
    client_street_address_number: str
    client_street_address: str
    client_city: str
    client_zipcode: str
    client_country: str
    annotator: int
    annotation_id: int
    created_at: datetime
    updated_at: datetime
    lead_time: float

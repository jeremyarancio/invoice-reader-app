from datetime import datetime, date
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field


class LabelStudioExportJSONMIN(BaseModel):
    id_: Annotated[int, Field(validation_alias="id")]
    image_path: Annotated[str, Field(validation_alias="image")]
    currency: str
    gross_amount: Annotated[float, BeforeValidator(lambda x: x[0]["number"])]
    vat: Annotated[float, BeforeValidator(lambda x: x[0]["number"])]
    issued_date: Annotated[
        date | None,
        BeforeValidator(
            lambda x: datetime.strptime(x[0]["datetime"], "%d-%m-%Y").date()
            if x
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

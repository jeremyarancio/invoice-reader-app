from datetime import datetime, date
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field

from parser.domain.parse import Annotation


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

    def to_annotation(self) -> Annotation:
        return Annotation(
            annotator_id=self.id_,
            image_uri=self.image_path,
            currency=self.currency,
            gross_amount=self.gross_amount,
            vat=self.vat,
            issued_date=self.issued_date,
            invoice_number=self.invoice_number,
            client_name=self.client_name,
            client_street_address_number=self.client_street_address_number,
            client_street_address=self.client_street_address,
            client_city=self.client_city,
            client_zipcode=self.client_zipcode,
            client_country=self.client_country,
            annotator=self.annotator,
            annotation_id=self.annotation_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            lead_time=self.lead_time,
        )

from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel

from parser.domain.parse import Annotation, ParsedData


class AnnotationStorageSchema(BaseModel):
    id_: UUID
    image_path: str
    currency: str
    gross_amount: float
    vat: float
    issued_date: date | None = None
    invoice_number: str
    client_name: str
    client_street_address_number: str
    client_street_address: str
    client_city: str
    client_zipcode: str
    client_country: str
    created_at: datetime
    updated_at: datetime

    def to_annotation(self) -> Annotation:
        return Annotation(
            image_uri=self.image_path,
            created_at=self.created_at,
            updated_at=self.updated_at,
            data=ParsedData(
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
            ),
        )

    @classmethod
    def from_annotation(cls, annotation: Annotation) -> "AnnotationStorageSchema":
        return cls(
            id_=1,
            image_path=annotation.image_uri,
            currency=annotation.data.currency,
            gross_amount=annotation.data.gross_amount,
            vat=annotation.data.vat,
            issued_date=annotation.data.issued_date,
            invoice_number=annotation.data.invoice_number,
            client_name=annotation.data.client_name,
            client_street_address_number=annotation.data.client_street_address_number,
            client_street_address=annotation.data.client_street_address,
            client_city=annotation.data.client_city,
            client_zipcode=annotation.data.client_zipcode,
            client_country=annotation.data.client_country,
            created_at=annotation.created_at,
            updated_at=annotation.updated_at,
        )

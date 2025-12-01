from datetime import datetime, date
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Annotation(BaseModel):
    id_: UUID = Field(default_factory=uuid4)
    annotator_id: int
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
    annotator: int
    annotation_id: int
    created_at: datetime
    updated_at: datetime
    lead_time: float

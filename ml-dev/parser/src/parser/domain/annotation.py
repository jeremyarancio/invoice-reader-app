from datetime import datetime, date
import re

from pydantic import BaseModel


class Annotation(BaseModel):
    image_name: str
    id_: int
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

    @classmethod
    def from_label_studio(cls, data: dict) -> "Annotation":
        """Parse annotation from Label Studio export format."""
        return cls(
            image_name=re.search(r"[^\/]-(.+png)$", data["image"]).group(1),  # type: ignore
            id_=data["id"],
            currency=data["currency"],
            gross_amount=float(data["gross_amount"][0]["number"]),
            vat=float(data["vat"][0]["number"]),
            issued_date=(
                datetime.strptime(data["issued_date"][0]["datetime"], "%d-%m-%Y").date()
                if data.get("issued_date")
                else None
            ),
            invoice_number=data["invoice_number"],
            client_name=data["client_name"],
            client_street_address_number=data["client_street_address_number"],
            client_street_address=data["client_street_address"],
            client_city=data["client_city"],
            client_zipcode=data["client_zipcode"],
            client_country=data["client_country"],
            annotator=data["annotator"],
            annotation_id=data["annotation_id"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            lead_time=data["lead_time"],
        )

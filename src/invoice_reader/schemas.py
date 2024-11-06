from typing import Annotated
from datetime import date
from pydantic import BaseModel


class Adresse(BaseModel):
    street: str
    zipcode: int
    city: str
    country: str


class Revenu(BaseModel):
    excluding_tax: float = None
    vat: Annotated[float, "In percentage: 20, 21, ..."] = None
    currency: str = "€"


class InvoiceMetadata(BaseModel):
    client_name: str = None
    client_adresse: Adresse = None
    revenu: Revenu = None
    invoiced_date: date = None

    def is_complete(self) -> bool:
        if all(self.model_dump().values()):
            return True
        return False


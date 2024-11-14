import os
from typing import Annotated
from datetime import date
import uuid

from pydantic import BaseModel, Field


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
    

class FileData(BaseModel):
    user_id: str
    filename: str = Field(pattern=r"^\w+\.\w{2,3}$", description=".pdf, .png, ...")
    file_id: str = uuid.uuid1()

    @property
    def file_format(self):
            return os.path.splitext(self.filename)[-1]


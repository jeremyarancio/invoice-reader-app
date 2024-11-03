from typing import Annotated
from datetime import date
from pydantic import BaseModel


class ClientAdresse(BaseModel):
    adresse: str
    zipcode: int
    city: str
    country: str


class Revenu(BaseModel):
    #TODO: Find a way to validate only two and compute the remaining one
    excluding_tax: float = None
    with_tax: float = None
    vat: Annotated[float, "In percentage: 20, 21, ..."] = None 


class InvoiceMetadata(BaseModel):
    client_name: str = None
    client_adresse: ClientAdresse = None
    revenu: Revenu = None
    invoiced_date: date = None
    complete: bool = False

    def is_complete(self) -> bool:
        if all(self.model_dump().values()):
            return True
        return False

    
    

    
from datetime import date
from typing import BinaryIO

import httpx
from pydantic import BaseModel

from invoice_reader import settings
from invoice_reader.app.exceptions import INVALID_EXTRACTED_DATA_EXCEPTION


class Address(BaseModel):
    street_address: str | None = None
    zipcode: str | None = None
    city: str | None = None
    country: str | None = None


class Invoice(BaseModel):
    gross_amount: float | None = None
    vat: int | None = None
    issued_date: date | None = None
    due_date: date | None = None
    invoice_number: str | None = None
    invoice_description: str | None = None
    currency: str | None = None


class Client(BaseModel):
    name: str | None = None
    address: Address | None = None


class Seller(BaseModel):
    name: str | None = None
    address: Address | None = None


class InvoiceExtraction(BaseModel):
    invoice: Invoice
    client: Client
    seller: Seller


def parse_invoice(file: BinaryIO) -> InvoiceExtraction:
    """Parse document using the /parser endpoint from the ML server."""
    files = {"upload_file": file}
    api_url = settings.ML_SERVER_URL + "/v1/parse"
    response = httpx.post(api_url, files=files)
    if response.status_code != 200:
        raise INVALID_EXTRACTED_DATA_EXCEPTION
    invoice_data = InvoiceExtraction.model_validate(response.json())
    return invoice_data

from pydantic import BaseModel

from invoice_reader.domain.client import Client
from invoice_reader.domain.parser import ParsedInvoiceData


class ParserResponse(BaseModel):
    """Return the invoice data and the retrieved client from the database, if any."""

    invoice: ParsedInvoiceData
    client: Client | None = None

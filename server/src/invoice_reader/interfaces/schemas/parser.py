from uuid import UUID

from pydantic import BaseModel

from invoice_reader.domain.invoice import InvoiceData


class ParserResponse(BaseModel):
    """Return the invoice data and the retrieved client from the database, if any."""

    invoice: InvoiceData
    client_id: UUID | None = None

from uuid import UUID

from pydantic import BaseModel

from invoice_reader.domain.parser import ParsedInvoiceData


class ParserResponse(BaseModel):
    """Return the invoice data and the retrieved client from the database, if any."""

    invoice: ParsedInvoiceData
    client_id: UUID | None = None

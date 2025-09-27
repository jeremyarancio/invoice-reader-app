from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from invoice_reader.domain.invoice import Invoice


class ClientData(BaseModel):
    client_name: str
    street_number: int
    street_address: str
    zipcode: str
    city: str
    country: str


class Client(BaseModel):
    id_: UUID = Field(default_factory=uuid4)
    user_id: UUID
    invoices: list[Invoice] = []
    data: ClientData

    @property
    def total_revenue(self) -> float:
        return sum(invoice.data.gross_amount for invoice in self.invoices)

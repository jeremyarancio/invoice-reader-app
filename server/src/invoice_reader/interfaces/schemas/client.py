from uuid import UUID

from pydantic import BaseModel

from invoice_reader.domain.client import Client, ClientData
from invoice_reader.domain.invoice import Currency


class ClientCreate(ClientData):
    pass


class ClientResponse(BaseModel):
    client_id: UUID
    data: ClientData

    @classmethod
    def from_client(cls, client: Client) -> "ClientResponse":
        return cls(
            client_id=client.id_,
            data=client.data,
        )


class ClientUpdate(BaseModel):
    data: ClientData


class PagedClientResponse(BaseModel):
    page: int
    per_page: int
    total: int
    clients: list[ClientResponse]


class ClientRevenueResponse(BaseModel):
    client_id: UUID
    n_invoices: int
    # In case of error with the Exchange rates service
    total_revenue: dict[Currency, float] | None = None

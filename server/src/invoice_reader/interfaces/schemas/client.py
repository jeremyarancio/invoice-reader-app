from uuid import UUID

from pydantic import BaseModel

from invoice_reader.domain.client import Client, ClientData
from invoice_reader.domain.invoice import Currency


class ClientCreate(ClientData):
    pass


class ClientResponse(BaseModel):
    client_id: UUID
    n_invoices: int
    total_revenue: dict[Currency, float]
    data: ClientData

    @classmethod
    def from_client(
        cls, client: Client, total_revenue: dict[Currency, float], n_invoices: int
    ) -> "ClientResponse":
        return cls(
            client_id=client.id_,
            data=client.data,
            n_invoices=n_invoices,
            total_revenue=total_revenue,
        )


class ClientUpdate(BaseModel):
    data: ClientData


class PagedClientResponse(BaseModel):
    page: int
    per_page: int
    total: int
    clients: list[ClientResponse]

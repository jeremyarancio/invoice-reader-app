from uuid import UUID

from pydantic import BaseModel

from invoice_reader.domain.client import Client, ClientData


class ClientCreate(ClientData):
    pass


class ClientResponse(BaseModel):
    client_id: UUID
    total_revenue: float = 0
    data: ClientData

    @classmethod
    def from_client(cls, client: Client) -> "ClientResponse":
        return cls(
            client_id=client.id_,
            total_revenue=client.total_revenue,
            data=client.data,
        )


class ClientUpdate(ClientData):
    pass


class PagedClientResponse(BaseModel):
    page: int
    per_page: int
    total: int
    clients: list[ClientResponse]

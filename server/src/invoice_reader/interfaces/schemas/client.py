from uuid import UUID

from pydantic import BaseModel

from invoice_reader.domain.client import ClientData


class ClientCreate(ClientData):
    pass


class ClientResponse(BaseModel):
    client_id: UUID
    total_revenue: float = 0
    data: ClientData


class ClientUpdate(ClientData):
    pass


class PagedClientResponse(BaseModel):
    page: int
    per_page: int
    total: int
    clients: list[ClientResponse]

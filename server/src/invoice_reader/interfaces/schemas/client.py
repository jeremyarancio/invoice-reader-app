from uuid import UUID

from pydantic import BaseModel

from invoice_reader.domain.client import ClientBase


class ClientCreate(ClientBase):
    pass


class ClientResponse(ClientBase):
    client_id: UUID
    total_revenue: float = 0

class ClientUpdate(ClientBase):
    pass


class PagedClientResponse(BaseModel):
    page: int
    per_page: int
    total: int
    data: list[ClientResponse]

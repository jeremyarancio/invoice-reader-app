from pydantic import BaseModel

from invoice_reader.domain.client import ClientBase


class ClientCreate(ClientBase):
    pass


class ClientResponse(ClientBase):
    pass


class ClientUpdate(ClientBase):
    pass


class PagedClientResponse(BaseModel):
    page: int
    per_page: int
    total: int
    data: list[ClientResponse]

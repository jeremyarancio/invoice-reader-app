import uuid

from pydantic import BaseModel


class ClientBase(BaseModel):
    client_name: str
    street_number: int
    street_address: str
    zipcode: int
    city: str
    country: str


class Client(ClientBase):
    client_id: uuid.UUID | None = None
    total_revenu: float | None = None


class ClientCreate(Client):
    pass


class ClientResponse(Client):
    pass


class PagedClientResponse(BaseModel):
    page: int
    per_page: int
    total: int
    data: list[ClientResponse]

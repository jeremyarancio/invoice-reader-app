import uuid

from pydantic import BaseModel


class Client(BaseModel):
    client_name: str
    street_number: int
    street_address: str
    zipcode: int
    city: str
    country: str


class ClientCreate(Client):
    pass


class ClientPresenter(Client):
    client_id: uuid.UUID | None
    total_revenu: float | None


class ClientResponse(Client):
    client_id: uuid.UUID
    total_revenu: float


class PagedClientResponse(BaseModel):
    page: int
    per_page: int
    total: int
    data: list[ClientResponse]

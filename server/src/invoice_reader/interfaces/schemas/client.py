from pydantic import BaseModel


class ClientBase(BaseModel):
    client_name: str
    street_number: int
    street_address: str
    zipcode: int
    city: str
    country: str


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

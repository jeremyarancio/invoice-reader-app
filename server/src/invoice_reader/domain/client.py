from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ClientBase(BaseModel):
    client_name: str
    street_number: int
    street_address: str
    zipcode: str
    city: str
    country: str


class Client(ClientBase):
    id_: UUID = Field(default_factory=uuid4)
    user_id: UUID
    total_revenue: float = Field(
        ge=0, default=0
    )  # TODO: Change into an Amount entity for currency conversion


class ClientUpdate(ClientBase):
    pass

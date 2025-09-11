from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from invoice_reader.domain.user import UserID


class ClientID(UUID):
    @classmethod
    def create(cls) -> "ClientID":
        return cls(uuid4().hex)


class ClientBase(BaseModel):
    client_name: str
    street_number: int
    street_address: str
    zipcode: int
    city: str
    country: str


class Client(ClientBase):
    id_: ClientID = Field(default_factory=ClientID.create)
    user_id: UserID
    total_revenue: float = Field(
        ge=0, default=0
    )  # TODO: Change into an Amount entity for currency conversion


class ClientUpdate(ClientBase):
    pass

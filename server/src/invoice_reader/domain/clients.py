from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ClientID(UUID):
    @classmethod
    def create(cls) -> "ClientID":
        return cls(uuid4().hex)


class BaseClient(BaseModel):
    client_name: str
    street_number: int
    street_address: str
    zipcode: int
    city: str
    country: str


class Client(BaseClient):
    client_id: ClientID = Field(default_factory=ClientID.create)
    user_id: UUID
    total_revenu: float = Field(
        ge=0, default=0
    )  # TODO: Change into an Amount entity for currency conversion


class ClientUpdate(BaseClient):
    pass

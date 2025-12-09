from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ClientData(BaseModel):
    client_name: str
    street_number: str
    street_address: str
    zipcode: str
    city: str
    country: str


class Client(BaseModel):
    id_: UUID = Field(default_factory=uuid4)
    user_id: UUID
    data: ClientData

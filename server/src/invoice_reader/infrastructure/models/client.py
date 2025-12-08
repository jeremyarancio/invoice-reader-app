from uuid import UUID

from sqlmodel import Field, SQLModel  # type: ignore


class ClientModel(SQLModel, table=True):
    __tablename__ = "client"  # type: ignore

    client_id: UUID = Field(primary_key=True)
    user_id: UUID = Field(foreign_key="user.user_id")
    client_name: str
    street_number: str
    street_address: str
    zipcode: str
    city: str
    country: str

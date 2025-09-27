from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id_: UUID = Field(default_factory=uuid4)
    email: EmailStr
    is_disabled: bool = False
    hashed_password: str

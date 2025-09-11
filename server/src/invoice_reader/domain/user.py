from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field


class UserID(UUID):
    @classmethod
    def create(cls) -> "UserID":
        return cls(uuid4().hex)


class User(BaseModel):
    id_: UserID = Field(default_factory=UserID.create)
    email: EmailStr
    is_disabled: bool = False
    hashed_password: str

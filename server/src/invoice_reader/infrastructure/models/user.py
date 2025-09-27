from uuid import UUID

from sqlmodel import Field, SQLModel  # type: ignore


class UserModel(SQLModel, table=True):
    __tablename__ = "user"  # type: ignore

    user_id: UUID = Field(primary_key=True)
    email: str
    is_disabled: bool = Field(default=False)
    hashed_password: str

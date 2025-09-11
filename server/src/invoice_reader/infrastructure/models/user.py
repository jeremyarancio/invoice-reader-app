from sqlmodel import Field, SQLModel  # type: ignore

from invoice_reader.domain.user import UserID


class UserModel(SQLModel, table=True):
    __tablename__ = "user"  # type: ignore

    user_id: UserID = Field(primary_key=True)
    email: str
    is_disabled: bool = Field(default=False)
    hashed_password: str

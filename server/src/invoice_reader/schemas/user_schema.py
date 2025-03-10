import uuid

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    user_id: uuid.UUID | None = None
    email: EmailStr
    is_disabled: bool | None = None
    hashed_password: str


class UserCreate(BaseModel):
    password: str = Field(
        ..., min_length=8, description="Password must be at least 8 characters"
    )
    email: EmailStr


class UserPresenter(User):
    pass


class UserResponse(BaseModel):
    user_id: uuid.UUID
    email: EmailStr

from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from invoice_reader.domain.user import User


class UserCreate(BaseModel):
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    email: EmailStr


class UserResponse(BaseModel):
    user_id: UUID
    email: EmailStr

    @classmethod
    def from_user(cls, user: User) -> "UserResponse":
        return cls(
            user_id=user.id_,
            email=user.email,
        )

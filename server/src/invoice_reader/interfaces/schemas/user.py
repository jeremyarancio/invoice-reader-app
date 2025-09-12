from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    email: EmailStr


class UserResponse(BaseModel):
    user_id: UUID
    email: EmailStr

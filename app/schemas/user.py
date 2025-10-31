from pydantic import BaseModel, EmailStr
from typing import Optional
from fastapi_users import schemas
from uuid import UUID

class UserRead(schemas.BaseUser[int]):
    id: UUID
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified : bool = False

    class Config:
        fromattributes = True

class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str

class UserUpdate(schemas.BaseUserUpdate):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    
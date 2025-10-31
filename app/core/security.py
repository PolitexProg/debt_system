# app/core/security.py

from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID # Импортируем UUID
from fastapi_users import BaseUserManager, UUIDIDMixin, FastAPIUsers
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

from app.core.config import settings
from app.db.models import User
from app.core.database import get_async_db
from app.schemas.user import UserRead, UserCreate, UserUpdate



async def get_user_db(db: AsyncSession = Depends(get_async_db)) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    yield SQLAlchemyUserDatabase(db, User)


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]): 
    reset_password_token_secret = settings.SECRET
    verification_token_secret = settings.SECRET

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.SECRET, 
        lifetime_seconds=settings.JWT_LIFETIME_SECONDS
    )

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager=get_user_manager,
    auth_backends=[auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import AsyncGenerator
from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine
from app.db.models import Base
from app.db.models import Debt, User, Settings
engine = create_async_engine(
    settings.DATABASE_URL,
    future=True,
)

AsyncSessionFactory = async_sessionmaker(   
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
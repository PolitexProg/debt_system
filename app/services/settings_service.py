from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.db.models import Settings
from app.schemas.settings import SettingsUpdate
from fastapi import HTTPException


async def get_or_create_settings(db: AsyncSession, user_id: UUID) -> Settings:
    """Get existing settings for a user or create default settings if none exist."""
    query = select(Settings).filter(Settings.user_id == user_id)
    result = await db.execute(query)
    db_settings = result.scalar_one_or_none()

    if db_settings:
        return db_settings
    
    new_settings = Settings(user_id=user_id)
    db.add(new_settings)
    await db.commit()
    await db.refresh(new_settings)

    return new_settings


async def update_settings(db: AsyncSession, user_id: UUID, update_data: SettingsUpdate) -> Settings:
    query = select(Settings).filter(Settings.user_id == user_id)
    result = await db.execute(query)
    db_settings = result.scalar_one_or_none()

    if not db_settings:
        raise HTTPException(
            status_code=404,
            detail="Settings for user not found"
        )

    update_data_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_data_dict.items():
        setattr(db_settings, key, value)

    await db.commit()
    await db.refresh(db_settings)

    return db_settings

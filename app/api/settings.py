from fastapi import APIRouter, Depends, status
from app.services import settings_service
from app.schemas.settings import SettingsRead, SettingsUpdate
from app.db.models import User, Settings
from app.core.database import get_async_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import current_active_user
from uuid import UUID


router = APIRouter(
    prefix='/api/settings',
    tags=['Settings']
)

@router.get('/', response_model=SettingsRead, status_code=status.HTTP_200_OK)
async def settings_read(
    db: AsyncSession = Depends(get_async_db),
    curr_user: User = Depends(current_active_user),
) -> SettingsRead:
    user_id: UUID = curr_user.id
    db_settings = await settings_service.get_or_create_settings(db, user_id)
    return SettingsRead.model_validate(db_settings)


@router.patch('/', response_model=SettingsRead, status_code=status.HTTP_200_OK)
async def user_settings_update(
    settings_data: SettingsUpdate,
    db: AsyncSession = Depends(get_async_db),
    curr_user: User = Depends(current_active_user)
) -> SettingsRead:
    user_id: UUID = curr_user.id
    db_settings = await settings_service.update_settings(db, user_id, settings_data)
    return SettingsRead.model_validate(db_settings)
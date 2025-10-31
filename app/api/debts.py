from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.core.security import current_active_user
from app.db.models import User

from app.schemas.debt import DebtRead, DebtCreate, DebtUpdate
from app.services import debt_service
from uuid import UUID

router = APIRouter(prefix="/api/debt", tags=["Debts"])

@router.post('/', response_model=DebtRead, status_code=status.HTTP_201_CREATED)
async def create_new_debt(
    debt_data: DebtCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(current_active_user)
):
    return await debt_service.create_debt(db, debt_data, current_user.id)

@router.get('/', response_model=list[DebtRead])
async def get_user_debts(
    debt_type: str = Query(None, description=''),
    person_name: str = Query(None, description=''),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(current_active_user)
):
    return await debt_service.get_debts(
        db,
        current_user.id,
        debt_type=debt_type,
        person_name=person_name
    )

@router.get('/{debt_id}', response_model=DebtRead)
async def get_one_debt(
    debt_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(current_active_user)
):
    return await debt_service.get_one_debt(db, debt_id, current_user.id)


@router.patch("/{debt_id}", response_model=DebtRead)
async def update_debt(debt_id: UUID, update_data: DebtUpdate, db: AsyncSession = Depends(get_async_db), current_user: User = Depends(current_active_user)):
    return await debt_service.update_debt(db, debt_id, current_user.id, update_data)

@router.delete('/{debt_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_debt(
    debt_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(current_active_user)
):
    await debt_service.delete_debt(db, debt_id, current_user.id)

    return




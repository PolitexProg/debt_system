from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from fastapi import status, HTTPException


from app.db.models import Debt, User
from app.schemas.debt import DebtCreate, DebtRead, DebtUpdate

async def get_debt_by_id_owner(db: AsyncSession, debt_id: UUID, user_id: UUID) -> Debt:
    stmt = select(Debt).where(Debt.id == debt_id, Debt.owner_id == user_id)
    result = await db.execute(stmt)
    db_debt = result.scalars().first()
    if not db_debt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Debt not found or access denied'
        )
    
    return db_debt


async def create_debt(db: AsyncSession, debt_data: DebtCreate, user_id: UUID) -> Debt:
    db_debt = Debt(**debt_data.model_dump(), owner_id=user_id)
    db.add(db_debt)
    await db.commit()
    await db.refresh(db_debt)

    return db_debt


async def get_debts(db: AsyncSession, user_id: UUID, debt_type: Optional[str]=None, person_name: Optional[str] = None):
    stmt = select(Debt).where(Debt.owner_id == user_id)
    if debt_type:
        stmt = stmt.where(Debt.debt_type == debt_type)

    if person_name:
        stmt = stmt.where(Debt.person_name.ilike(f'%{person_name}'))

    result = await db.execute(stmt)

    return list(result.scalars().all())


async def get_one_debt(db: AsyncSession, debt_id: UUID, user_id: UUID) -> Debt:
    return await get_debt_by_id_owner(db, debt_id, user_id)


async def update_debt(db: AsyncSession, debt_id: UUID, user_id: UUID, update_data: DebtUpdate) -> Debt:
    db_debt = await get_debt_by_id_owner(db, debt_id, user_id)

    update_data_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_data_dict.items():
        setattr(db_debt, key, value)

    await db.commit()

    await db.refresh(db_debt)
    return db_debt

async def delete_debt(db: AsyncSession, debt_id: UUID, user_id: UUID) -> bool:
    db_debt = await get_debt_by_id_owner(db, debt_id, user_id)
    
    await db.delete(db_debt)
    
    await db.commit()
    return True


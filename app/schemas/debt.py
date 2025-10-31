from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from uuid import UUID

class DebtBase(BaseModel):
    debt_type:  str
    person_name: str
    currency: str
    amount: float
    description: Optional[str] = None
    date_due: Optional[date] = None
    is_settled: bool = False



class DebtCreate(DebtBase):
    pass

class DebtUpdate(DebtBase):
    debt_type: Optional[str] = None
    person_name: Optional[str] = None
    currency: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    date_due: Optional[date] = None
    is_settled: Optional[bool] = False

class DebtRead(DebtBase):
    id: UUID
    owner_id: UUID
    date_incurred: datetime

    class Config:
        from_attributes = True


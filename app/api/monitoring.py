# app/api/monitoring.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.database import get_async_db
from app.core.security import current_active_user
from app.db.models import User
from app.schemas.monitoring import MonitoringRead, CurrencySummary  
from app.services import monitoring_service

router = APIRouter(prefix="/api/monitoring", tags=["Monitoring"])

@router.get("/", response_model=MonitoringRead, status_code=status.HTTP_200_OK)
async def get_monitoring_data(
    db: AsyncSession = Depends(get_async_db), 
    current_user: User = Depends(current_active_user)
):
    user_id = current_user.id
    summary_dict = await monitoring_service.get_user_summary(db, user_id)

    summary_list = []
    
    for currency, data in summary_dict.items():
        currency_data = {
            "currency": currency,
            "total_owed_to": data.get("total_owed_to", 0.0),
            "total_owed_by": data.get("total_owed_by", 0.0),
            "net_balance": data.get("net_balance", 0.0)
        }
        
        
        summary_list.append(CurrencySummary(**currency_data))
    return MonitoringRead(summary_by_currency=summary_list)
from pydantic import BaseModel
from typing import List, Dict

class CurrencySummary(BaseModel):
    currency: str
    total_owed_to: float
    total_owed_by: float
    net_balance: float

    class Config:
        from_attributes = True

class MonitoringRead(BaseModel):
    summary_by_currency: List[CurrencySummary]

    class Conifg:
        from_attributes = True
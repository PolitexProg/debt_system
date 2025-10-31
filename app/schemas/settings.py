from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
class SettingsRead(BaseModel):
    user_id: UUID
    default_currency: str
    reminder_time: str

    class Config:
        from_attributes = True

class SettingsCreate(BaseModel):
    default_currency: str = "USD"
    reminder_time: str = "09:00"

class SettingsUpdate(BaseModel):
    
    default_currency: Optional[str] = Field(None, max_length=5)
    reminder_time: Optional[str] = None
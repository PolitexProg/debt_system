from sqlalchemy import Column, Date, String, Boolean, DateTime,ForeignKey, Float, func
from sqlalchemy.orm import relationship, DeclarativeBase
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy_utils import UUIDType
import uuid


class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    settings = relationship("Settings", back_populates='user', uselist=False)
    debts = relationship("Debt", back_populates="owner")

class Settings(Base):
    __tablename__ = "settings"
    user_id = Column(UUIDType(binary=False), ForeignKey("users.id"), primary_key=True, default=uuid.uuid4)
    default_currency = Column(String(5), nullable=False, default="USD")
    reminder_time = Column(String, default="09:00")

    user = relationship("User", back_populates="settings")


class Debt(Base):
    __tablename__ = 'debt'

    id = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4)
    owner_id = Column(UUIDType(binary=False), ForeignKey('users.id'))


    debt_type = Column(String, nullable=False)
    person_name = Column(String, nullable=False)
    currency = Column(String(5), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String(1024))
    
    date_incurred = Column(DateTime, default=func.now())
    date_due = Column(Date)
    is_settled = Column(Boolean, default=False)

    owner = relationship("User", back_populates='debts')



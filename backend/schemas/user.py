from datetime import time
from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    about: Optional[str] = None
    notes: Optional[str] = None
    telegram_id: int
    morning_notification: Optional[time] = None
    evening_notification: Optional[time] = None


class UserBase(BaseModel):
    id: int
    name: Optional[str] = None
    age: Optional[int] = None
    about: Optional[str] = None
    notes: Optional[str] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    about: Optional[str] = None
    notes: Optional[str] = None
    morning_notification: Optional[time] = None
    evening_notification: Optional[time] = None


class UserRead(UserBase):
    id: int
    morning_notification: Optional[str] = None
    evening_notification: Optional[str] = None

    class Config:
        from_attributes = True

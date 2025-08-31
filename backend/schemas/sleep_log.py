from datetime import date, datetime, time
from typing import Optional

from pydantic import BaseModel


class SleepLogBase(BaseModel):
    sleep_quality: Optional[str] = None
    feeling: Optional[str] = None
    energy: Optional[int] = None


class SleepLogCreate(SleepLogBase):
    user_id: int
    bedtime: str
    wake_time: str


class SleepLogRead(SleepLogBase):
    user_id: int
    bedtime: time
    wake_time: time
    date: date

    class Config:
        from_attributes = True

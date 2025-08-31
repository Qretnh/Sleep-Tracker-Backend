from datetime import time
from typing import Optional

from pydantic import BaseModel, field_serializer

from backend.db.models.sleep_goal import GoalType


class SleepGoalBase(BaseModel):
    goal_type: GoalType
    value_time: Optional[str] = None
    value_hours: Optional[int] = None


class SleepGoalCreate(SleepGoalBase):
    user_id: int


class SleepGoalUpdate(BaseModel):
    value_time: Optional[str] = None
    value_hours: Optional[int] = None


class SleepGoalRead(SleepGoalBase):
    id: int
    user_id: int
    value_time: Optional[time] = None

    @field_serializer("value_time")
    def serialize_time(self, v: Optional[time], _info):
        return v.strftime("%H:%M") if v else None

    class Config:
        from_attributes = True

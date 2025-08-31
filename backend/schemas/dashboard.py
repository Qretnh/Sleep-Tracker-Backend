from pydantic import BaseModel


class SleepDurationRead(BaseModel):
    date: str
    duration_hours: float

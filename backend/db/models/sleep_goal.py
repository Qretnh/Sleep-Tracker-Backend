import enum

from sqlalchemy import BigInteger, Column, Enum, ForeignKey, Integer, Time
from sqlalchemy.orm import relationship

from backend.db.models.base import Base


class GoalType(enum.Enum):
    SLEEP_BEFORE = "sleep_before"
    WAKE_BEFORE = "wake_before"
    SLEEP_HOURS = "sleep_hours"


class SleepGoal(Base):
    __tablename__ = "sleep_goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))

    goal_type = Column(Enum(GoalType), nullable=False)
    value_time = Column(Time, nullable=True)
    value_hours = Column(Integer, nullable=True)

    user = relationship("User", back_populates="goals")

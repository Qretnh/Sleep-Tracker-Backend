from sqlalchemy import BigInteger, Column, Integer, String, Text, Time
from sqlalchemy.orm import relationship

from backend.db.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)

    name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    about = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    morning_notification = Column(Time, nullable=True)
    evening_notification = Column(Time, nullable=True)

    goals = relationship(
        "SleepGoal", back_populates="user", cascade="all, delete-orphan"
    )
    sleep_logs = relationship(
        "SleepLog", back_populates="user", cascade="all, delete-orphan"
    )
    reports = relationship(
        "SleepReport", back_populates="user", cascade="all, delete-orphan"
    )

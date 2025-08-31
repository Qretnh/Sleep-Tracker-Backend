from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Text,
    Time,
)
from sqlalchemy.orm import relationship

from backend.db.models.base import Base


class SleepLog(Base):
    __tablename__ = "sleep_logs"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))

    date = Column(Date, default=datetime.utcnow, nullable=False)
    bedtime = Column(Time, nullable=False)
    wake_time = Column(Time, nullable=False)

    sleep_quality = Column(Text, nullable=True)
    feeling = Column(Text, nullable=True)
    energy = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="sleep_logs")

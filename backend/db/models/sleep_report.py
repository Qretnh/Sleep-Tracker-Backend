from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship

from backend.db.models.base import Base


class SleepReport(Base):
    __tablename__ = "sleep_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))

    week_start = Column(Date, nullable=True)
    week_end = Column(Date, nullable=True)

    short_summary = Column(Text, nullable=False)
    long_summary = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reports")

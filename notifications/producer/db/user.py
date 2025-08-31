from sqlalchemy import BigInteger, Column, Integer, String, Text, Time
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)

    name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    about = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    morning_notification = Column(Time, nullable=True)
    evening_notification = Column(Time, nullable=True)

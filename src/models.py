from datetime import date
from sqlalchemy import Column, Integer, String, Boolean, Date

from src.database import Base

class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    money = Column(Integer)
    profit = Column(Boolean, default=False)
    date = Column(Date, default=date.today)
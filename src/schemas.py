from pydantic import BaseModel, Field
from datetime import date as day

class DealBase(BaseModel):
    title: str
    money: int = Field(..., gt=0)
    profit: bool = False
    date: day = Field(default_factory=day.today)

class Deal(DealBase):
    id: int

    class Config:
        from_attributes = True

class DealCreate(DealBase):
    pass
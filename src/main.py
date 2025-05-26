from src.database import SessionLocal, engine
from src import models, schemas

from fastapi import FastAPI, Depends, HTTPException, Query, status
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/deals/', response_model=schemas.Deal)
def create_deal(deal: schemas.DealCreate, db: Session = Depends(get_db)):
    db_deal = models.Deal(**deal.dict())
    db.add(db_deal)
    db.commit()
    db.refresh(db_deal)
    return db_deal

@app.get('/deals/', response_model=List[schemas.Deal])
def read_deals(
    type: Optional[str] = Query(None),
    start: Optional[date] = Query(None),
    end: Optional[date] = Query(None),
    db: Session = Depends(get_db)):
    query = db.query(models.Deal)
    if type:
        if type == "income":
            query = query.filter(models.Deal.profit==True)
        elif type == "expense":
            query = query.filter(models.Deal.profit==False)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"Type '{type}' not found")
    if start and end:
        query = query.filter(and_(models.Deal.date>=start, models.Deal.date<=end))
    elif start:
        query = query.filter(models.Deal.date>=start)
    elif end:
        query = query.filter(models.Deal.date <= end)
    deals = query.all()
    return deals

@app.put('/deals/{id}', response_model=schemas.Deal)
async def update_deal(id: int, deal: schemas.DealCreate, db: Session=Depends(get_db)):
    db_deal = db.query(models.Deal).filter(models.Deal.id == id).first()
    if not db_deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    for field, value in deal.dict().items():
        setattr(db_deal, field, value)

    db.commit()
    db.refresh(db_deal)
    return db_deal

@app.delete('/deals/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_deal(id: int, db: Session = Depends(get_db)):
    deal = db.query(models.Deal).filter(models.Deal.id == id).first()
    if not deal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deal with id {id} not found"
        )
    db.delete(deal)
    db.commit()

@app.get('/balance')
async def get_balance(
    balance: Optional[int] = 0,
    start: Optional[date] = Query(None),
    end: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Deal)
    if start and end:
        query = query.filter(and_(models.Deal.date>=start, models.Deal.date<=end))
    elif start:
        query = query.filter(models.Deal.date>=start)
    elif end:
        query = query.filter(models.Deal.date <= end)
    deals = query.all()
    for act in deals:
        balance = balance + act.money if act.profit == True else balance - act.money
    return f"Current balance {balance}"
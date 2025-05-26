from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

DBURL = 'postgresql://postgres:ebgmlv001352@localhost:5432/family'

engine = create_engine(DBURL)

SessionLocal = sessionmaker(autocommit=False, autoflush= False, bind=engine)

Base = declarative_base()
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Boolean, Column, Float, String, Integer

app = FastAPI()

#SqlAlchemy Setup
SQLALCHEMY_DATABASE_URL = 'sqlite+pysqlite:///./db.sqlite3:'
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DBBeers(Base):
    __tablename__ = 'beers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    maker = Column(String(30), nullable=True)
    description = Column(String(50))
    scanned_id = Column(String(15),index=True)
    rating = Column(Integer())
    img_url = Column(String(255))

Base.metadata.create_all(bind=engine)

class Beers(BaseModel):
    name: str
    maker: str
    description: Optional[str] = None
    scanned_id : str
    rating : str
    img_url : str


    class Config:
        orm_mode = True

def get_beer(db: Session, beer_scanned_id: int):
    return db.query(DBBeers).where(DBBeers.scanned_id == beer_scanned_id).first()

def get_beers(db: Session):
    return db.query(DBBeers).all()

def create_beer(db: Session, beers: Beers):
    db_beers = DBBeers(**beers.dict())
    db.add(db_beers)
    db.commit()
    db.refresh(db_beers)

    return db_beers


@app.post('/beers/', response_model=Beers)
def create_beers_view(beers: Beers, db: Session = Depends(get_db)):
    db_beers = create_beer(db, beers)
    return db_beers

@app.get('/beers/', response_model=List[Beers])
def get_beers_view(db: Session = Depends(get_db)):
    return get_beers(db)

@app.get('/beers/{scanned_id}',response_model=Beers)
def get_beers_view(scanned_id: int, db: Session = Depends(get_db)):
    return get_beer(db, scanned_id)

@app.get('/')
async def root():
    return {'message': 'Hello World!'}
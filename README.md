# BeerAPI
Python FastAPI to store favourite beers 

This is a training exercise to use FastAPI to store and retrieve beer information fron a SQLite database. 
This example is borrowed with thanks from https://codingnomads.co/blog/python-fastapi-tutorial  

The goal of the project is to scan the barcode of a beer and read or commit information to a database.

The Model for the database is 

class DBBeers(Base):
    __tablename__ = 'beers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    maker = Column(String(30), nullable=True)
    description = Column(String(50))
    scanned_id = Column(String(15),index=True)
    rating = Column(Integer())
    img_url = Column(String(255))
    
This project provides an API for another frontend application. Details to follow.

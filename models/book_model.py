from sqlalchemy import Column, Integer, String
from database.db import Base

class BookDB(Base):
    __tablename__ = "books"  # name of the table in the database

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    year = Column(Integer)


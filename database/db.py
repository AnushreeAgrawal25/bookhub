from sqlalchemy import create_engine                        #to create a connection to your database.
from sqlalchemy.ext.declarative import declarative_base     #base class from which all your database models will inherit
from sqlalchemy.orm import sessionmaker                     #creates a session(crud operation)

DATABASE_URL = "sqlite:///./books.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# This function is required to avoid the import error
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
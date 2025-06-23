#importing fastAPI
from fastapi import FastAPI
from routers import books

app = FastAPI(
    title="BookHub API",
    description=" A FastAPI-powered system to manage books and search titles via Google Books.",
    version="1.0.0",
    contact={
        "name": "Anushree",
        "email": "anushree250504@gmail.com",
    }
)

app.include_router(books.router)

#binding the table with the app
from database.db import Base, engine
from models.book_model import BookDB

# This will create the books table in books.db (if it doesn't exist)
Base.metadata.create_all(bind=engine)



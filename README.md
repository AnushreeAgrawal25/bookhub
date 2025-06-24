BookHub – A FastAPI-Based Book Management System

BookHub is a RESTful API that allows users to manage books with full CRUD functionality, Google Books search integration, and live deployment using Render. Built with FastAPI, SQLAlchemy, and SQLite, it also includes Swagger documentation and automated testing.

Live Demo: 

Swagger UI:[https://bookhub-fastapi.onrender.com/docs](https://bookhub-fastapi.onrender.com/docs)  
Home: [https://bookhub-fastapi.onrender.com](https://bookhub-fastapi.onrender.com)

Features:
-  Create, read, update, and delete book entries
-  Search books using Google Books API
-  SQLite database using SQLAlchemy ORM
-  Pydantic for data validation
-  Pytest test suite with in-memory DB
-  Live Swagger UI for interactive API testing
- Deployed on Render

Setup Instructions (Local): 

 Requirements:
- Python 3.10 or newer
- pip
  
Installation:
git clone https://github.com/AnushreeAgrawal25/bookhub.git

>cd bookhub

>pip install -r requirements.txt

>uvicorn main:app --reload

API Endpoints:

- GET	/ :	Welcome message

- GET	/books :	List all books

- POST	/books :	Add a new book

- GET	/books/{book_id} :	Retrieve a book by ID

- PUT	/books/{book_id} :	Update book details by ID

- DELETE	/books/{book_id} :	Delete book by ID

- GET	/search :	Search books via Google Books API

 Example Usage:
- Add a Book (POST /books)
  
{
  "title": "Atomic Habits",
  "author": "James Clear",
  "year": 2018
}

- Google Books Search (GET /search?query=harry+potter)
  
Response:
[
  {
    "title": "Harry Potter and the Philosopher's Stone",
    "authors": ["J.K. Rowling"],
    "publishedDate": "1997"
  },
]

 Author:

Developed by [Anushree Agrawal](https://github.com/AnushreeAgrawal25)

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from models.book import Book  # Pydantic model
from models.book_model import BookDB  # SQLAlchemy model
from services.google_books import search_google_books
from database.db import SessionLocal
from sqlalchemy import asc, desc
from models.error import ErrorResponse



#to create the session for the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

books = []

@router.get("/", summary="Welcome endpoint", response_description="Greeting message")
def read_root():
    return {"message": "Welcome to BookHub!"}

@router.get(
    "/books",
    response_model=List[Book],
    summary="Get a list of books",
    description="Returns all books from the database. You can paginate, sort, or search using query parameters."
)
def get_books(
    skip: int = 0,
    limit: int = 10,
    sort_by: str = Query("id", enum=["id", "title", "author", "year"]),
    sort_order: str = Query("asc", enum=["asc", "desc"]),
    search: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(BookDB)

    # Optional search by title or author
    if search:
        query = query.filter(
            (BookDB.title.ilike(f"%{search}%")) |
            (BookDB.author.ilike(f"%{search}%"))
        )

    # Sorting
    order_clause = asc(getattr(BookDB, sort_by)) if sort_order == "asc" else desc(getattr(BookDB, sort_by))
    query = query.order_by(order_clause)

    # Pagination
    books = query.offset(skip).limit(limit).all()

    return books


@router.get(
    "/books/{book_id}",
    response_model=Book,
    responses={404: {"model": ErrorResponse}},
    summary="Get a book by ID",
    description="Returns book details if the ID exists, otherwise returns 404"
)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book



@router.post(
    "/books",
    response_model=Book,
    summary="Add a new book",
    description="Creates a new book entry in the database. Requires title, author, and publication year."
)
def create_book(book: Book, db: Session = Depends(get_db)):
    new_book = BookDB(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.put(
    "/books/{book_id}",
    response_model=Book,
    responses={404: {"model": ErrorResponse}},
    summary="Update a book",
    description="Updates a book's title, author, or year by ID"
)
def update_book(book_id: int, updated_book: Book, db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book.title = updated_book.title
    book.author = updated_book.author
    book.year = updated_book.year
    db.commit()
    db.refresh(book)
    return book



@router.delete(
    "/books/{book_id}",
    responses={
        200: {"description": "Book successfully deleted"},
        404: {"model": ErrorResponse}
    },
    summary="Delete a book",
    description="Deletes a book from the database by its ID"
)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(book)
    db.commit()
    return {"message": "Book deleted"}



@router.get("/search", summary="Search books using Google Books API", response_description="List of books from Google")
def search_books(query: str = Query(..., min_length=1)):
    results = search_google_books(query)
    if results is None:
        raise HTTPException(status_code=502, detail="Failed to fetch from Google Books API")
    return {"results": results}


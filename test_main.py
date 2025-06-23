#basic test cases
from fastapi.testclient import TestClient
from main import app
from routers.books import books
from models.book import Book

client = TestClient(app)

sample_book = Book(id=1, title="Atomic Habits", author="James Clear", year=2018)
updated_book = Book(id=1, title="Atomic Habits - Updated", author="James Clear", year=2020)

def setup_function():
    books.clear()
    books.append(sample_book)

def test_create_book():
    books.clear()
    response = client.post("/books", json=sample_book.dict())
    assert response.status_code == 200
    assert response.json() == sample_book.dict()

def test_get_all_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert sample_book.dict() in response.json()

def test_get_book_by_id_exists():
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json() == sample_book.dict()

def test_get_book_by_id_not_found():
    response = client.get("/books/999")
    assert response.status_code == 200
    assert response.json() == {"error": "Book not found"}

def test_update_book_success():
    response = client.put("/books/1", json=updated_book.dict())
    assert response.status_code == 200
    assert response.json() == updated_book.dict()

def test_update_book_not_found():
    response = client.put("/books/999", json=sample_book.dict())
    assert response.status_code == 200
    assert response.json() == {"error": "Book not found"}

def test_delete_book_success():
    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Book deleted"}

def test_delete_book_not_found():
    response = client.delete("/books/999")
    assert response.status_code == 200
    assert response.json() == {"error": "Book not found"}


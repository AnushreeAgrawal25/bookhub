import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database.db import Base, get_db
from models.book_model import BookDB

# Setup a temporary SQLite test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Recreate the schema on each run
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Override the dependency and define the client
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# Test cases
def test_create_book():
    response = client.post("/books", json={
        "title": "Test Driven Development",
        "author": "Kent Beck",
        "year": 2002
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Driven Development"
    assert data["author"] == "Kent Beck"
    assert data["year"] == 2002
    assert "id" in data

def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_book_by_id():
    create = client.post("/books", json={
        "title": "Clean Code",
        "author": "Robert Martin",
        "year": 2008
    })
    book_id = create.json()["id"]
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Clean Code"

def test_update_book():
    create = client.post("/books", json={
        "title": "Old Book",
        "author": "Old Author",
        "year": 1990
    })
    book_id = create.json()["id"]
    response = client.put(f"/books/{book_id}", json={
        "title": "New Title",
        "author": "New Author",
        "year": 2025
    })
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"

def test_delete_book():
    create = client.post("/books", json={
        "title": "Temp Book",
        "author": "To Delete",
        "year": 2020
    })
    book_id = create.json()["id"]
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted"

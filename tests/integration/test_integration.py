import pytest
import httpx
from bookstore.main import app
from bookstore.database import Book, UserCredentials, engine, SessionLocal
from sqlalchemy.orm import Session

@pytest.fixture(scope="module")
def test_db():
    engine.dispose()
    Book.metadata.create_all(engine)
    UserCredentials.metadata.create_all(engine)
    yield SessionLocal()
    Book.metadata.drop_all(engine)
    UserCredentials.metadata.drop_all(engine)

@pytest.fixture
def client():
    return httpx.AsyncClient(base_url="http://test")

@pytest.mark.asyncio
async def test_integration_signup_login_create_book_get_books(client, test_db):
    async with client as ac:
        # Signup
        signup_response = await ac.post("/signup", json={"email": "integration@example.com", "password": "password123"})
        assert signup_response.status_code == 200

        # Login
        login_response = await ac.post("/login", json={"email": "integration@example.com", "password": "password123"})
        assert login_response.status_code == 200
        access_token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # Create Book
        create_book_response = await ac.post("/books/", json={"name": "Integration Book", "author": "Integration Author", "published_year": 2024, "book_summary": "Integration Summary"}, headers=headers)
        assert create_book_response.status_code == 200
        book_id = create_book_response.json()["id"]

        # Get Book by ID
        get_book_response = await ac.get(f"/books/{book_id}", headers=headers)
        assert get_book_response.status_code == 200
        assert get_book_response.json()["name"] == "Integration Book"

        # Get All Books
        get_all_books_response = await ac.get("/books/", headers=headers)
        assert get_all_books_response.status_code == 200
        assert len(get_all_books_response.json()) == 1

        # Update Book
        update_book_response = await ac.put(f"/books/{book_id}", json={"name": "Updated Book", "author": "Updated Author", "published_year": 2025, "book_summary": "Updated Summary"}, headers=headers)
        assert update_book_response.status_code == 200
        assert update_book_response.json()["name"] == "Updated Book"

        # Delete Book
        delete_book_response = await ac.delete(f"/books/{book_id}", headers=headers)
        assert delete_book_response.status_code == 200

        # Verify Book is deleted
        get_deleted_book_response = await ac.get(f"/books/{book_id}", headers=headers)
        assert get_deleted_book_response.status_code == 404

@pytest.mark.asyncio
async def test_integration_login_failure(client, test_db):
    async with client as ac:
        # Signup
        await ac.post("/signup", json={"email": "failure@example.com", "password": "password123"})

        # Login with incorrect password
        login_response = await ac.post("/login", json={"email": "failure@example.com", "password": "wrongpassword"})
        assert login_response.status_code == 400

@pytest.mark.asyncio
async def test_integration_unauthorized_book_access(client, test_db):
    async with client as ac:
        # Try to access books without authentication
        response = await ac.get("/books/")
        assert response.status_code == 403

        response = await ac.post("/books/", json={"name": "Unauthorized Book", "author": "Unauthorized Author", "published_year": 2024, "book_summary": "Summary"})
        assert response.status_code == 403

@pytest.mark.asyncio
async def test_integration_health_check(client, test_db):
    async with client as ac:
        response = await ac.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "up"}

@pytest.mark.asyncio
async def test_integration_signup_duplicate_email(client, test_db):
    async with client as ac:
        # Signup
        await ac.post("/signup", json={"email": "duplicate@example.com", "password": "password123"})
        # Signup with duplicate email
        response = await ac.post("/signup", json={"email": "duplicate@example.com", "password": "password456"})
        assert response.status_code == 400
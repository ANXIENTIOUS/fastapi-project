from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Глобальные переменные (как в примере)
client.book_id = 0


# CREATE
def test_create_book():
    response = client.post(
        "/v2/books/",
        json={
            "title": "Test Book",
            "author": "Tester",
            "year": 2024,
            "description": "Test description"
        }
    )

    assert response.status_code == 201

    data = response.json()
    client.book_id = data["book_id"]

    assert data["title"] == "Test Book"


# READ ONE
def test_get_book():
    response = client.get(f"/v2/books/{client.book_id}")

    assert response.status_code == 200

    data = response.json()
    assert data["book_id"] == client.book_id


# READ ALL
def test_get_books():
    response = client.get("/v2/books/")

    assert response.status_code in [200, 204]


# UPDATE
def test_update_book():
    response = client.patch(
        f"/v2/books/{client.book_id}",
        json={
            "year": 2000
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["year"] == 2000


# DELETE
def test_delete_book():
    response = client.delete(f"/v2/books/{client.book_id}")

    assert response.status_code == 200


# CHECK DELETE
def test_deleted_book_not_found():
    response = client.get(f"/v2/books/{client.book_id}")

    assert response.status_code == 404

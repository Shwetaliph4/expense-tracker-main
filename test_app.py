import pytest
from app import app, expenses

@pytest.fixture(autouse=True)
def clear_expenses():
    expenses.clear()
    yield
    expenses.clear()

def test_home():
    assert app.test_client().get("/").status_code == 200

def test_add_expense():
    response = app.test_client().post(
        "/expenses",
        json={"title": "Food", "amount": 250}
    )
    assert response.status_code == 201
    assert response.json["amount"] == 250

def test_get_expenses():
    client = app.test_client()
    client.post(
        "/expenses",
        json={"title": "Travel", "amount": 100}
    )
    assert len(client.get("/expenses").json) == 1

def test_invalid_expense():
    response = app.test_client().post(
        "/expenses",
        json={"title": "Food", "amount": -10}
    )
    assert response.status_code == 400

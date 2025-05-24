from fastapi import status
from .utils import (
    override_get_db,
    override_get_current_user,
    client,
    TestingSessionLocal,
    test_todo,
)
from main import app
from db.models import Todos
from routers.r_todos import get_current_user, get_db


# Apply dependency overrides to the FastAPI app.
# These ensure that during tests, the overridden dependencies are used.
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_one_authenticated_not_found(test_todo):
    response = client.get("/todo/500")

    assert response.status_code == 404
    assert response.json() == {"detail": "id no. 500 does not exist"}


def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1")

    # Assert that the response status code is HTTP 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Assert that the JSON response matches the expected todo data, including id
    assert response.json() == {
        "id": test_todo.id,  # dynamically use the ID of the test todo
        "complete": False,
        "title": "t1",
        "description": "d1",
        "priority": 5,
        "owner_id": 1,
    }


def test_read_all_authenticated(test_todo):
    # Send a GET request to the /todo endpoint using the test client
    response = client.get("/todo")

    # Assert that the response status code is HTTP 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Assert that the JSON response matches the expected todo data, including id
    assert response.json() == [
        {
            "id": test_todo.id,  # dynamically use the ID of the test todo
            "complete": False,
            "title": "t1",
            "description": "d1",
            "priority": 5,
            "owner_id": 1,
        }
    ]


def test_create_todo(test_todo):
    request_data = {
        "complete": True,
        "title": "t2",
        "description": "d1d2",
        "priority": 5,
        "owner_id": 1,
    }

    response = client.post("/todo/", json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()

    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.priority == request_data.get("priority")
    assert model.complete == request_data.get("complete")


def test_update_todo(test_todo):
    request_data = {
        "complete": False,
        "title": "t1",
        "description": "d1-updated",
        "priority": 5,
        "owner_id": 1,
    }
    response = client.put("/todo/1", json=request_data)
    assert response.status_code == 200 or response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == request_data.get("title")


def test_update_todo_not_found(test_todo):
    request_data = {
        "complete": False,
        "title": "t1",
        "description": "d1-updated",
        "priority": 5,
        "owner_id": 1,
    }
    response = client.put("/todo/500", json=request_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "id no. 500 does not exist"}


def test_delete_authenticated(test_todo):
    response = client.delete("/todo/1")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_authenticated_not_found(test_todo):
    response = client.delete("/todo/500")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "id no. 500 does not exist"}

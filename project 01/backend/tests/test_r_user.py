from fastapi import status
from .utils import (
    override_get_db,
    override_get_current_user,
    client,
    TestingSessionLocal,
    test_todo,
    test_user,
)
from main import app
from db.models import Todos, Users
from routers.r_todos import get_current_user, get_db


# Apply dependency overrides to the FastAPI app.
# These ensure that during tests, the overridden dependencies are used.
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "user1"
    assert response.json()["firstname"] == "user1"
    assert response.json()["lastname"] == "user1"
    assert response.json()["role"] == "admin"
    assert response.json()["phone"] == 1245678245
    assert response.json()["email"] == "user1@user1.com"


def test_change_password_success(test_user):
    response = client.put(
        "/user/password",
        json={
            "password": "user1",
            "new_password": "user1Pass",
        },
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put(
        "/user/password",
        json={
            "password": "user55555",
            "new_password": "user1Pass",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change"}


# def test_admin_delete_todo(test_todo):
#     response = client.delete("admin/todo/1")
#     assert response.status_code == status.HTTP_204_NO_CONTENT

#     db = TestingSessionLocal()
#     model = db.query(Todos).filter(Todos.id == 1).first()
#     assert model is None


# def test_admin_delete_todo_not_found(test_todo):
#     response = client.delete("admin/todo/500")
#     assert response.status_code == status.HTTP_404_NOT_FOUND
#     assert response.json() == {"detail": "Todo id no. 500 does not exist"}

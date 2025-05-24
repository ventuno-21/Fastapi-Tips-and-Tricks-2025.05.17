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


def test_admin_read_all_authenticated(test_todo):
    response = client.get("admin/todo")
    assert response.status_code == status.HTTP_200_OK
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


def test_admin_delete_todo(test_todo):
    response = client.delete("admin/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_admin_delete_todo_not_found(test_todo):
    response = client.delete("admin/todo/500")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo id no. 500 does not exist"}

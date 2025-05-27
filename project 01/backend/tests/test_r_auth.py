from fastapi import status, HTTPException
from .utils import (
    override_get_db,
    override_get_current_user,
    client,
    TestingSessionLocal,
    test_user,
)
from main import app
from routers.r_auth import (
    create_access_token,
    authenticate_user,
    get_db,
    SECRET_KEY,
    ALGORITHM,
    get_current_user,
)
from datetime import timedelta
from jose import jwt
import pytest

# Apply dependency overrides to the FastAPI app.
# These ensure that during tests, the overridden dependencies are used.
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, "user1", db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    not_existent_user = authenticate_user("user2", "user1", db)
    assert not_existent_user is False

    wrong_password_user = authenticate_user("user1", "wrongPassword", db)
    assert wrong_password_user is False


def test_create_access_token():
    username = "user2"
    user_id = 1
    role = "user"
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)

    decoded_token = jwt.decode(
        token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False}
    )

    assert decoded_token["username"] == username
    assert decoded_token["id"] == user_id
    assert decoded_token["role"] == role


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {"username": "user50", "id": 1, "role": "admin"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token)
    assert user == {"username": "user50", "id": 1, "role": "admin"}


@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    encode = {"role": "user"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as e:
        await get_current_user(token=token)

    assert e.value.status_code == 401
    assert e.value.detail == "Could not validate a user"

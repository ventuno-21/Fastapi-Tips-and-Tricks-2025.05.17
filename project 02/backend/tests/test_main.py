import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from ..main import app

# from ..main import app
from fastapi import status


@pytest.mark.asyncio
async def test_return_health_check2(client: AsyncClient):
    response = await client.get("/healthy2")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "HEALTHY"}


@pytest.fixture(scope="module")
def sync_client():
    return TestClient(app)


def test_return_health_check(sync_client: TestClient):
    response = sync_client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "HEALTHY"}


# client = TestClient(app)


# def test_return_health_check():
#     response = client.get("/healthy")
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json() == {"status": "HEALTHY"}

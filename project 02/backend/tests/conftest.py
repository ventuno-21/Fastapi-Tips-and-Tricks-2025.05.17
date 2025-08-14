import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from ..db.async_engine_sqlmodel_postgres import get_session

# from app.database.session import get_session
from ..main import app

# from .tests import example

# Test database
engine = create_async_engine(url="sqlite+aiosqlite:///:memory:")

test_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session_override():
    async with test_session() as session:
        yield session


@pytest_asyncio.fixture(scope="session")
async def client():
    async with AsyncClient(
        # app=app,
        base_url="http://test",
        transport=ASGITransport(app),
    ) as client:
        yield client


# @pytest_asyncio.fixture(scope="session")
# async def client():
#     async with  (
#         transport=ASGITransport(app),
#         base_url="http://test",
#     ) as client:
#         yield client

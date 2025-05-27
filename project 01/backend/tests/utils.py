from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker
from fastapi import status
from fastapi.testclient import TestClient
import pytest

# from ..db.sync_engine import Base
from db.sync_engine import Base
from db.models import Todos, Users
from main import app
from routers.r_todos import get_current_user, get_db
from routers.r_auth import bcrypt_context

# Define the test database URL using SQLite (in-memory or file-based for testing).
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"

# Create a SQLAlchemy engine for the test database.
# StaticPool is used to ensure all connections share the same in-memory database,
# and check_same_thread=False allows usage in different threads (needed for testing).
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create a session factory bound to the test engine.
# This will be used to interact with the database during tests.
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Ensure all database tables are created before running tests.
# Base should be your declarative base used to define models.
# Make sure to uncomment and define Base properly elsewhere in your code.
# Base = declarative_base()
Base.metadata.create_all(bind=engine)


# Dependency override for getting a DB session during tests.
# This replaces the application's `get_db` dependency with a version that uses the test DB.
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependency override for simulating an authenticated user in tests.
# Returns a mock user dictionary instead of requiring actual authentication.
def override_get_current_user():
    return {"username": "user1", "id": 1, "role": "admin"}


# Create a TestClient for the FastAPI app.
# This allows sending test requests to the app without running a live server.
client = TestClient(app)


# @pytest.fixture
# def test_todo():
#     # Create test data
#     db = TestingSessionLocal()
#     todo = Todos(
#         title="t1", description="d1", id=1, priority=5, owner_id=1, complete=False
#     )
#     db.add(todo)
#     db.commit()
#     db.refresh(todo)
#     yield todo
#     # Clean up after test using ORM
#     db.query(Todos).delete()
#     db.commit()
#     db.close()


@pytest.fixture
def test_todo():
    # Create a new Todo instance with test data (title, description, priority, etc.)
    todo = Todos(title="t1", description="d1", priority=5, owner_id=1, complete=False)

    # Create a new database session for testing
    db = TestingSessionLocal()

    # Add the new todo to the session
    db.add(todo)

    # Commit the session to save the todo to the test database
    db.commit()

    # Provide the todo instance to the test functions that use this fixture
    yield todo

    # Cleanup: delete all todos from the database after the test runs
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    # Create a new User instance with test data (title, description, priority, etc.)
    user = Users(
        username="user1",
        email="user1@user1.com",
        firstname="user1",
        lastname="user1",
        role="admin",
        phone=1245678245,
        hash_password=bcrypt_context.hash("user1"),
    )
    # Create a new database session for testing
    db = TestingSessionLocal()

    # Add the new user to the session
    db.add(user)

    # Commit the session to save the todo to the test database
    db.commit()

    # Provide the todo instance to the test functions that use this fixture
    yield user

    # Cleanup: delete all todos from the database after the test runs
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()

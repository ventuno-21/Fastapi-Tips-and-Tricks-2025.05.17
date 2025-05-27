from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import (
    sessionmaker,
    declarative_base,
    DeclarativeBase,
    MappedAsDataclass,
)

# for sync codes
# SQLALCHEMY_DATABASE_URL = "sqlite:///./databse.db"
# for async codes
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./databse.db"

# for sync codes
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# for async codes
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

# for sync codes
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# for async codes
SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# for sync codes
# Base = declarative_base()
# for async codes
class Base(DeclarativeBase, MappedAsDataclass):
    pass


# for sync codes
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# for async codes
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

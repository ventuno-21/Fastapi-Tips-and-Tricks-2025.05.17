import os
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

# Load environment variables from .env file
load_dotenv()

POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")


#  SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# POSTGRES_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
POSTGRES_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"


# Create a database engine to connect with database
engine = create_async_engine(
    # database type/dialect and file name
    url=POSTGRES_URL,
    # Log sql queries
    echo=True,
)


async def create_db_tables():
    async with engine.begin() as connection:
        from .sqlmodel_models import Shipment, Seller  # noqa: F401

        await connection.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]

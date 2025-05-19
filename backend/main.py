from fastapi import FastAPI, Body
from enum import Enum
from typing import Optional
from pydantic import BaseModel
from routers.r_users import router as user_router
from routers.r_test import router as test_router
from db.engine import Base, engine
from contextlib import asynccontextmanager


# @app.on_event("startup")
# async def init_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/users", tags=["user"])
app.include_router(test_router, prefix="/test", tags=["test"])

from fastapi import FastAPI, Body
from db.sync_engine import Base, engine
from enum import Enum
from typing import Optional
from pydantic import BaseModel
from routers.r_users import router as user_router
from routers.r_test import router as test_router
from routers.r_todos import router as todo_router
from routers.r_auth import router as auth_router
from routers.r_admin import router as admin_router
from routers.r_users import router as user_router
from db import models
from contextlib import asynccontextmanager

# @app.on_event("startup")
# async def init_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#         yield


# app = FastAPI(lifespan=lifespan)

app = FastAPI()

# models.Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(todo_router, prefix="/todo", tags=["todo"])
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(test_router, prefix="/test", tags=["test"])


# If you use alembic, you can ignore below line
# models.Base.metadata.create_all(engine)

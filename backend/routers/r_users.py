from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import Annotated
from db.sync_engine import get_db
from db.models import Todos, Users
from starlette import status
from pydantic import BaseModel, Field
from jose import JWTError, jwt
from datetime import timedelta, datetime, timezone
from .r_auth import get_current_user
from passlib.context import CryptContext

router = APIRouter()

db_dependancy = Annotated[Session, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"])


router = APIRouter()


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=5)


@router.get(
    "/", status_code=status.HTTP_200_OK, description="Description of register function"
)
async def get_user(user: user_dependancy, db: db_dependancy):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")

    return db.query(Users).filter(Users.id == user.get("id")).first()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependancy,
    db: db_dependancy,
    user_verification: UserVerification,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hash_password):
        raise HTTPException(status_code=401, detail="Error on password change")
    else:
        user_model.hash_password = bcrypt_context.hash(user_verification.new_password)
        db.add(user_model)
        db.commit()
        db.refresh(user_model)
        return user_model


@router.post("/login", description="Description of register function")
async def register():
    return {"message": "hi"}


@router.put("/", description="Description of register function")
async def get_update_profile():
    return {"message": "hi"}

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


router = APIRouter()

db_dependancy = Annotated[Session, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all_todos(user: user_dependancy, db: db_dependancy):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication failed")
    else:
        return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependancy, db: db_dependancy, todo_id: int = Path(gt=0)
):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication failed")
    else:
        todo = db.query(Todos).filter(Todos.id == todo_id).first()
        if todo is None:
            raise HTTPException(
                status_code=404, detail=f"Todo id no. {todo_id} does not exist"
            )
        else:
            db.query(Todos).filter(Todos.id == todo_id).delete()
            db.commit()

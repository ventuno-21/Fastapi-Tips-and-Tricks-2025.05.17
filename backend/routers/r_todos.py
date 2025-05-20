from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import Annotated
from db.sync_engine import get_db
from db.models import Todos
from starlette import status
from pydantic import BaseModel, Field


router = APIRouter()

db_dependancy = Annotated[Session, Depends(get_db)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=2, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@router.get("/")
async def all_todos(db: db_dependancy):
    return db.query(Todos).all()


@router.get(
    "/{todo_id}",
    description="Request a specific TODO",
    status_code=status.HTTP_200_OK,
)
async def read_todo(db: db_dependancy, todo_id: int):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo is not None:
        return todo
    else:
        raise HTTPException(status_code=404, detail=f"id no. {todo_id} does not exist")


@router.post("/")
async def create_todo(db: db_dependancy, todo_request: TodoRequest):
    todo = Todos(**todo_request.model_dump())
    db.add(todo)
    db.commit()
    return todo_request


@router.put("/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(
    db: db_dependancy, todo_request: TodoRequest, todo_id: int = Path(gt=0)
):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo is None:
        raise HTTPException(status_code=404, detail=f"id no. {todo_id} does not exist")
    else:
        todo.title = todo_request.title
        todo.description = todo_request.description
        todo.priority = todo_request.priority
        todo.complete = todo_request.complete

        db.add(todo)
        db.commit()

        return todo_request


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependancy, todo_id: int = Path(gt=0)):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo is not None:
        db.query(Todos).filter(Todos.id == todo_id).delete()
        db.commit()
    else:
        raise HTTPException(status_code=404, detail=f"id no. {todo_id} does not exist")

from fastapi import APIRouter, Depends, HTTPException, Path, Request
from sqlalchemy.orm import Session
from typing import Annotated
from db.sync_engine import get_db
from db.models import Todos
from starlette import status
from pydantic import BaseModel, Field
from .r_auth import get_current_user
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()

db_dependancy = Annotated[Session, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(get_current_user)]

templates = Jinja2Templates(directory="templates")


class TodoRequest(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=2, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@router.get("/test")
async def test(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/")
async def all_todos(user: user_dependancy, db: db_dependancy):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication is failed")
    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()


@router.get(
    "/{todo_id}",
    description="Request a specific TODO",
    status_code=status.HTTP_200_OK,
)
async def read_todo(user: user_dependancy, db: db_dependancy, todo_id: int):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication is failed")
    todo = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
    if todo is not None:
        return todo
    else:
        raise HTTPException(status_code=404, detail=f"id no. {todo_id} does not exist")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(
    user: user_dependancy,
    db: db_dependancy,
    todo_request: TodoRequest,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication is failed")
    todo = Todos(**todo_request.model_dump(), owner_id=user.get("id"))
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependancy,
    db: db_dependancy,
    todo_request: TodoRequest,
    todo_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication is failed")
    todo = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )

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
async def delete_todo(
    user: user_dependancy, db: db_dependancy, todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication is failed")
    todo = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
    if todo is not None:
        db.query(Todos).filter(Todos.id == todo_id).filter(
            Todos.owner_id == user.get("id")
        ).delete()
        db.commit()
    else:
        raise HTTPException(status_code=404, detail=f"id no. {todo_id} does not exist")

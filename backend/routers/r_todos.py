from fastapi import APIRouter, Depends, HTTPException, Path, Request, Form
from sqlalchemy.orm import Session
from typing import Annotated
from db.sync_engine import get_db
from db.models import Todos
from starlette import status
from starlette.responses import RedirectResponse
from pydantic import BaseModel, Field
from .r_auth2 import get_current_user
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()

db_dependancy = Annotated[Session, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(get_current_user)]

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def read_all_todos(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        print("read_all_todos/if/use is none")
        return RedirectResponse(url="/auth2", status_code=status.HTTP_302_FOUND)

    todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()

    return templates.TemplateResponse(
        "home.html", {"request": request, "todos": todos, "user": user}
    )


@router.get("/add-todo", response_class=HTMLResponse)
async def add_todo_get(request: Request):
    return templates.TemplateResponse("add-todo.html", {"request": request})


@router.post("/add-todo", response_class=HTMLResponse)
async def add_todo_post(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    priority: str = Form(...),
    db: Session = Depends(get_db),
):
    user = await get_current_user(request)
    if user is None:
        print("read_all_todos/if/use is none")
        return RedirectResponse(url="/auth2", status_code=status.HTTP_302_FOUND)
    todo = Todos()
    todo.title = title
    todo.description = description
    todo.priority = priority
    todo.complete = False
    todo.owner_id = user.get("id")

    db.add(todo)
    db.commit()

    return RedirectResponse(url="/todo", status_code=status.HTTP_302_FOUND)


@router.get("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo_get(request: Request, todo_id: int, db: db_dependancy):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    context = {"request": request, "todo": todo}
    return templates.TemplateResponse("edit-todo.html", context)


@router.post("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo_post(
    db: db_dependancy,
    request: Request,
    todo_id: int,
    title: str = Form(...),
    description: str = Form(...),
    priority: str = Form(...),
    # db: Session = Depends(get_db),
):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    todo.title = title
    todo.description = description
    todo.priority = priority

    db.add(todo)
    db.commit()

    return RedirectResponse(url="/todo", status_code=status.HTTP_302_FOUND)


@router.get("/delete/{todo_id}", response_class=HTMLResponse)
async def delete_todo_post(
    db: db_dependancy,
    request: Request,
    todo_id: int,
):
    user = await get_current_user(request)
    if user is None:
        print("read_all_todos/if/use is none")
        return RedirectResponse(url="/auth2", status_code=status.HTTP_302_FOUND)
    todo = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )

    if todo is None:
        return RedirectResponse(url="/todo", status_code=status.HTTP_302_FOUND)
    else:
        db.query(Todos).filter(Todos.id == todo_id).delete()
        db.commit()

        return RedirectResponse(url="/todo", status_code=status.HTTP_302_FOUND)


@router.get("/complete/{todo_id}", response_class=HTMLResponse)
async def complete_todo_get(
    db: db_dependancy,
    request: Request,
    todo_id: int,
):
    user = await get_current_user(request)
    if user is None:
        print("read_all_todos/if/use is none")
        return RedirectResponse(url="/auth2", status_code=status.HTTP_302_FOUND)
    todo = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )

    todo.complete = not todo.complete
    db.commit()

    return RedirectResponse(url="/todo", status_code=status.HTTP_302_FOUND)


# ******************** Todos API functionalities ********************


class TodoRequest(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=2, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@router.get("/api/")
async def all_todos(user: user_dependancy, db: db_dependancy):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication is failed")
    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()


@router.get(
    "/api/{todo_id}",
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


@router.post("/api/", status_code=status.HTTP_201_CREATED)
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


@router.put("/api/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
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


@router.delete("/api/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
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

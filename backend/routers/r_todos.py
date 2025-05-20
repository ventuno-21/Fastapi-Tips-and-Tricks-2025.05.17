from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from db.sync_engine import get_db
from db.models import Todos

router = APIRouter()

db_dependancy = Annotated[Session, Depends(get_db)]


@router.get("/")
async def all_todos(db: db_dependancy):
    return db.query(Todos).all()

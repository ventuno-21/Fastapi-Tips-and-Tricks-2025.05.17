from fastapi import APIRouter, Body
from enum import Enum
from typing import Optional
from pydantic import BaseModel
from routers.r_users import router as user_router
from db.engine import Base, engine
from contextlib import asynccontextmanager


router = APIRouter()


class CreatePostIn(BaseModel):
    title: str
    content: str


class foodEnum(str, Enum):
    fruits = "fruits"
    vegetables = "vegetables"
    dairy = "dairy"


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


BOOKS = [
    Book(1, "t1", "a1", "d1", 4),
    Book(2, "t2", "a2", "d2", 4),
    Book(3, "t3", "a3", "d3", 1),
    Book(4, "t4", "a4", "d4", 2),
    Book(5, "t5", "a5", "d5", 5),
]

items_dict = [{"item_one": "one"}, {"item_two": "two"}, {"item_three": "three"}]


@router.get("/", description="Description of this function", deprecated=True)
async def root():
    return {"message": "hi"}


@router.get("/foods/{food_name}")
async def get_food(food_name: foodEnum):
    if food_name == foodEnum.vegetables:
        return {"food_name": food_name, "message": "thats a  healthy choice"}
    if food_name.value == "fruits":
        return {"food_name": food_name, "message": "thats a  healthy choice"}

    return {"food_name": food_name, "message": "thats a healthy choice"}


@router.get("/items/")
async def list_items(skip: int = 0, limit: int = 10):
    return items_dict[skip : skip + limit]


@router.post("/create/")
async def create_post(post: CreatePostIn = Body()):
    return post


@router.post("/path/{y}")
async def xyz(x: int, y: str, z: Optional[int] = None):
    """
    x => is a QUERY parameter & is not optioanl, it has to be sent in URL
    y => is a PATH parameter & is not optioanl, it has to be sent in URL
    z => is a QUERY parameter & is  optioanl, & if you want you can dont send it in url
    """
    return {"it worked": f"x:{x} + y:{y} + z:{z}"}


@router.post("/path2/{y}")
async def xyz_with_body(x: int, y: str, z: Optional[int] = None, my_body=Body()):
    """
    x => is a QUERY parameter & is not optioanl, it has to be sent in URL
    y => is a PATH parameter & is not optioanl, it has to be sent in URL
    z => is a QUERY parameter & is  optioanl, & if you want you can dont send it in url
    my_body => Post method can have a body(But get method cannot have a body), here body is not optional

    """
    return {"xyz": f"x:{x} + y:{y} + z:{z}", "body": my_body}


@router.post("/path3/{y}")
async def xyz_with_optional_body(
    x: int, y: str, z: Optional[int] = None, my_body=Body(default=None)
):
    """
    x => is a QUERY parameter & is not optioanl, it has to be sent in URL
    y => is a PATH parameter & is not optioanl, it has to be sent in URL
    z => is a QUERY parameter & is  optioanl, & if you want you can dont send it in url
    my_body => Post method can have a body(But get method cannot have a body), here body is optional
    """
    return {"xyz": f"x:{x} + y:{y} + z:{z}", "body": my_body}

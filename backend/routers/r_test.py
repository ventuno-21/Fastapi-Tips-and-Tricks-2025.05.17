from fastapi import APIRouter, Body, Path
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
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
    # id: int
    # title: str
    # author: str
    # description: str
    # rating: int

    def __init__(self, id: int, title: str, author: str, description: str, rating: str):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    # id: Optional[int] = Field(title="id is not necessary to mention")
    id: Optional[int] = None
    title: str = Field(min_length=2)
    author: str = Field(min_length=2)
    description: str = Field(min_length=2, max_length=200)
    rating: int = Field(gt=0, lt=6)

    class Config:
        """
        You can pass a dict to json_schema_extra to add extra information to the JSON schema
        """

        json_schema_extra = {
            "example": {
                "title": "Vampire Dairy",
                "author": "Who knows who I am",
                "description": "A book about spooky girl inside a castle with magic wand",
                "rating": 5,
            }
        }


books = [
    Book(1, "t1", "a1", "d1", 4),
    Book(2, "t2", "a2", "d2", 4),
    Book(3, "t3", "a3", "d3", 1),
    Book(4, "t4", "a4", "d4", 2),
    Book(5, "t5", "a5", "d5", 5),
    Book(6, "t6", "a6", "d6", 5),
]

items_dict = [{"item_one": "one"}, {"item_two": "two"}, {"item_three": "three"}]


@router.get("/books")
async def all_books():
    return books


@router.get("/books/{book_id}")
async def single_book(book_id: int = Path(gt=0)):
    for b in books:
        if b.id == book_id:
            return b


@router.post("/create-book")
async def create_book(add_book=Body()):
    """
    This endpoint is based on Python class
    &
    It will not show SCHEMA in body of Swagger
    """
    books.append(add_book)
    return add_book


@router.delete("/books/{book_id}")
async def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(books)):
        if books[i].id == book_id:
            books.pop(i)
            break


@router.post("/create-book2")
async def create_book2(add_book: BookRequest):
    """
    This endpoint validation is based on Pydantic model
    &
    It will show Schema in body of Swagger
    """
    # print(f"=====> new book type: {type(add_book)}")
    # We should add new_book to Book class, because out items in books list expected Book class type
    # books.append(add_book)
    new_book = Book(**add_book.model_dump())
    books.append(assaign_correct_id(new_book))
    print(f"=====> new book type after add it to Book class: {type(new_book)}")
    print(new_book)
    print(f"convert to dictonary: {new_book.__dict__}")

    return new_book


def assaign_correct_id(book: Book):
    if len(books) > 0:
        book.id = books[-1].id + 1
    else:
        book.id = 1
    return book


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

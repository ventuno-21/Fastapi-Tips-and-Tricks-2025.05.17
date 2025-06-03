from db.sync_engine import Base
from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column

# from .aasync_engine import Base
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey


# class User(Base):
#     __tablename__ = "users"

#     password: Mapped[str] = mapped_column()
#     id: Mapped[int] = mapped_column(primary_key=True, index=True)
#     username: Mapped[str | None] = mapped_column(
#         unique=True, default=None, nullable=True
#     )


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    role = Column(String)
    hash_password = Column(String)
    is_active = Column(Boolean, default=False)
    phone = Column(Integer)


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

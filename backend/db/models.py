from db.sync_engine import Base
from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column

# from .aasync_engine import Base
from sqlalchemy import Column, Integer, Boolean, String


# class User(Base):
#     __tablename__ = "users"

#     password: Mapped[str] = mapped_column()
#     id: Mapped[int] = mapped_column(primary_key=True, index=True)
#     username: Mapped[str | None] = mapped_column(
#         unique=True, default=None, nullable=True
#     )


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    complete = Column(Boolean, default=False)

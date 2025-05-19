from sqlalchemy.orm import Mapped, mapped_column
from .engine import Base
from dataclasses import dataclass


class User(Base):
    __tablename__ = "users"

    password: Mapped[str] = mapped_column()
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str | None] = mapped_column(
        unique=True, default=None, nullable=True
    )

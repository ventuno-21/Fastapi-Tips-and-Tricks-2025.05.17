from enum import Enum
from pydantic import BaseModel, Field
from ..db.sqlmodel_models import ShipmentStatus


class BaseShipment(BaseModel):
    content: str
    weight: float = Field(le=25)
    destination: int


class Example(BaseModel):
    content: str


class ShipmentRead(BaseShipment):
    status: ShipmentStatus


class ShipmentCreate(BaseShipment):
    pass


class ShipmentUpdate(BaseModel):
    content: str | None = Field(default=None)
    weight: float | None = Field(default=None, le=25)
    destination: int | None = Field(default=None)
    status: ShipmentStatus

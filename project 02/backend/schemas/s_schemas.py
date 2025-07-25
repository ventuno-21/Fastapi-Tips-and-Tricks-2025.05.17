from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from ..db.sqlmodel_models import ShipmentStatus, ShipmentEvent
from uuid import UUID


class BaseShipment(BaseModel):
    content: str
    weight: float = Field(le=25)
    destination: int


class Example(BaseModel):
    content: str


class ShipmentRead(BaseShipment):
    id: UUID
    estimated_delivery: datetime | None = Field(default=None)
    timeline: list[ShipmentEvent]


class ShipmentCreate(BaseShipment):
    pass


class ShipmentUpdate(BaseModel):
    content: str | None = Field(default=None)
    weight: float | None = Field(default=None, le=25)
    location: int | None = Field(default=None)
    description: str | None = Field(default=None)
    status: ShipmentStatus
    estimated_delivery: datetime | None = Field(default=None)

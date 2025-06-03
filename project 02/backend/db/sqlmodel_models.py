from datetime import datetime
from enum import Enum
from sqlmodel import Field, SQLModel
from pydantic import EmailStr


class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


class Seller(SQLModel, table=True):

    id: int = Field(default=None, primary_key=True)
    name: str

    email: EmailStr
    password_hash: str


# Inherit SQLModel and set table = True
# to make a table in database
class Shipment(SQLModel, table=True):
    # Optional table name
    __tablename__ = "shipment"

    """
        Primary key with default value will be
        assigned and incremented automatically
    """
    id: int = Field(default=None, primary_key=True)

    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime


"""
some example of schemas in pydanatic basemodel that we have:
    class BaseShipment(BaseModel):
        content: str
        weight: float = Field(le=25)
        destination: int


    class ShipmentUpdate(BaseModel):
        content: str | None = Field(default=None)
        weight: float | None = Field(default=None, le=25)
        destination: int | None = Field(default=None)
        status: ShipmentStatus


=====================================================
example of sqlalchemy model:

    class Todos(Base):
        __tablename__ = "todos"

        id = Column(Integer, primary_key=True, index=True)
        title = Column(String)
        description = Column(String)
        priority = Column(Integer)
        complete = Column(Boolean, default=False)
        owner_id = Column(Integer, ForeignKey("users.id"))



"""

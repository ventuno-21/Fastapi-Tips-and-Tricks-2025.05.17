from datetime import datetime
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship, Column
from pydantic import EmailStr
from uuid import uuid4, UUID
from sqlalchemy.dialects import postgresql


class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


class Seller(SQLModel, table=True):
    # Uses default_factory=uuid4 for id fields to avoid null issues.
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    # id: UUID = Field(sa_column=Column(postgresql.UUID, default=None, primary_key=True))
    # id: int = Field(default=None, primary_key=True)
    name: str
    address: str | None = None
    email: EmailStr
    password_hash: str

    shipments: list["Shipment"] = Relationship(
        back_populates="seller",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


# Inherit SQLModel and set table = True
# to make a table in database
class Shipment(SQLModel, table=True):
    # Optional table name
    __tablename__ = "shipment"

    """
        Primary key with default value will be
        assigned and incremented automatically
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    # id: UUID = Field(sa_column=Column(postgresql.UUID, default=None, primary_key=True))
    # id: int = Field(default=None, primary_key=True)

    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime
    seller_id: UUID = Field(foreign_key="seller.id")  # model name should be lowecase
    # Many-to-one relationship with Seller model, linking each shipment to a seller
    # back_populates links to the 'shipments' field in the Seller model
    # sa_relationship_kwargs={"lazy": "selection"} optimizes SQLAlchemy query loading
    seller: "Seller" = Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


# shipment = Shipment()
# session.get(Seller, shipment.seller_id)

# seller Shipment(seller_id=seller.id)


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

from datetime import datetime
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship, Column
from pydantic import EmailStr
from uuid import uuid4, UUID
from sqlalchemy.dialects import postgresql
from sqlalchemy import ARRAY, INTEGER


class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"
    cancelled = "cancelled"


class User(SQLModel):
    name: str
    email: EmailStr
    """
    Field(exclude=True) → This tells Pydantic to ignore this field when 
    generating output with .dict(), .json(), or when sending data via an API.
    
    user = User(name="21", email="21@example.com", password_hash="s0me#h45h")
    print(user.dict())
    # Output: {'name': '21', 'email': '21@example.com'}
    # password_hash is excluded automatically
    """
    password_hash: str = Field(exclude=True)
    address: str | None = None


class Seller(User, table=True):
    __tablename__ = "seller"
    # Uses default_factory=uuid4 for id fields to avoid null issues.
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    # id: UUID = Field(sa_column=Column(postgresql.UUID, default=None, primary_key=True))
    # id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )
    address: str | None = Field(default=None)
    zip_code: int | None = Field(default=None)
    shipments: list["Shipment"] = Relationship(
        back_populates="seller",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class DeliveryPartner(User, table=True):
    __tablename__ = "delivery_partner"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )
    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )
    """
    By default, SQLModel infers the database column type from the Python type. 
    However, list[int] doesn’t have a direct mapping to a standard SQL type 
    across all databases, and SQLModel might NOT  automatically use PostgreSQL’s 
    ARRAY type.
    Using sa_column allows you to explicitly tell SQLModel to use SQLAlchemy’s
    ARRAY(INTEGER) type, ensuring compatibility with PostgreSQL’s array functionality.
    
    The combination of list[int] in Python and ARRAY(INTEGER) in 
    the database ensures that only lists of integers are stored, providing type
    safety at both the application and database levels.
    SQLAlchemy handles serialization/deserialization between Python’s 
    list[int] and PostgreSQL’s INTEGER[].
    
    Since you’re using Alembic for migrations, specifying sa_column=Column(ARRAY(INTEGER))
    ensures that Alembic generates the correct DDL (Data Definition Language) 
    for the serviceable_zip_codes column as an INTEGER[] in PostgreSQL when 
    creating or altering the table.
    Without this, Alembic might not correctly interpret the field, leading to 
    migration errors or incorrect schema definitions.
    
    You can skip sa_column for simple types (e.g., str, int, float) where SQLModel 
    infers the correct SQL type (e.g., VARCHAR, INTEGER).
    For complex types like arrays, explicit sa_column is necessary to ensure
    correctness.
    """
    serviceable_zip_codes: list[int] = Field(
        sa_column=Column(ARRAY(INTEGER)),
    )
    max_handling_capacity: int
    shipments: list["Shipment"] = Relationship(
        back_populates="delivery_partner",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    @property
    def active_shipments(self):
        return [
            shipment
            for shipment in self.shipments
            if shipment.status != ShipmentStatus.delivered
            or shipment.status != ShipmentStatus.cancelled
        ]

    @property
    def current_handling_capacity(self):
        return self.max_handling_capacity - len(self.active_shipments)


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
    estimated_delivery: datetime
    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )
    client_contact_email: EmailStr
    client_contact_phone: int | None
    # status: ShipmentStatus
    timeline: list["ShipmentEvent"] = Relationship(
        back_populates="shipment",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    seller_id: UUID = Field(foreign_key="seller.id")  # model name should be lowecase
    # Many-to-one relationship with Seller model, linking each shipment to a seller
    # back_populates links to the 'shipments' field in the Seller model
    # sa_relationship_kwargs={"lazy": "selection"} optimizes SQLAlchemy query loading
    seller: "Seller" = Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    delivery_partner_id: UUID = Field(
        foreign_key="delivery_partner.id",
    )
    delivery_partner: "DeliveryPartner" = Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    @property
    def status(self):
        return self.timeline[-1].status if len(self.timeline) > 0 else None


class ShipmentEvent(SQLModel, table=True):
    __tablename__ = "shipment_event"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )
    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )

    location: int
    status: ShipmentStatus
    description: str | None = Field(default=None)

    shipment_id: UUID = Field(foreign_key="shipment.id")
    shipment: Shipment = Relationship(
        back_populates="timeline",
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

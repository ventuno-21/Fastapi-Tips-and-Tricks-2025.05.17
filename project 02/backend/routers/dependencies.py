from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.async_engine_sqlmodel_postgres import get_session
from ..operations.o_shipment import ShipmentService


# Asynchronous database session dep annotation
SessionDep = Annotated[AsyncSession, Depends(get_session)]


# Shipment service dep
def get_shipment_service(session: SessionDep):
    """
    Defines a dependency function get_shipment_service that
    takes an AsyncSession (via SessionDep) and returns a ShipmentService instance.

    Components:

    session: SessionDep:
    The function expects an AsyncSession injected via SessionDep.
    The Annotated type ensures FastAPI resolves get_session to provide the session.

    ShipmentService: A custom service class (not shown but implied) that encapsulates
    business logic for shipment operations (e.g., CRUD operations on the shipment table).

    return ShipmentService(session):
    Instantiates and returns a ShipmentService object,
    passing the session to its constructor.

    Purpose: Provides a service layer to abstract database operations,
    promoting separation of concerns. The service likely handles queries like retrieving,
    creating, or updating shipments.
    """
    return ShipmentService(session)


# Shipment service dep annotation
"""
Defines a type alias ServiceDep that represents a ShipmentService instance 
obtained via get_shipment_service.

Components:
Annotated: 
Combines the ShipmentService type with Depends(get_shipment_service) metadata.

ShipmentService:
The service class returned by get_shipment_service.

Depends(get_shipment_service): 
Ensures FastAPI calls get_shipment_service to provide the ShipmentService instance,
which in turn depends on SessionDep (resolving to an AsyncSession).

ServiceDep: 
A reusable type alias for injecting ShipmentService into endpoints or other dependencies.

Purpose: Allows endpoints to inject a ShipmentService instance with a pre-configured 
session, streamlining access to shipment-related business logic.
"""
ServiceDep = Annotated[
    ShipmentService,
    Depends(get_shipment_service),
]

from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..db.async_engine_sqlmodel_postgres import get_session
from ..db.redis import is_jti_blacklisted
from ..db.sqlmodel_models import Seller
from ..operations.o_seller import SellerService
from ..operations.o_shipment import ShipmentService
from ..utils.token import decode_access_token

# Asynchronous database session dep annotation
SessionDep = Annotated[AsyncSession, Depends(get_session)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/seller/token")


# Access token data dep
async def get_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    data = decode_access_token(token)

    if data is None or await is_jti_blacklisted(data["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
        )

    return data


# Logged In Seller
async def get_current_seller(
    token_data: Annotated[dict, Depends(get_access_token)],
    session: SessionDep,
):
    return await session.get(Seller, token_data["user"]["id"])


SellerDep = Annotated[Seller, Depends(get_current_seller)]


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


# Seller service dep
def get_seller_service(session: SessionDep):
    return SellerService(session)


# Seller service dep annotation
SellerServiceDep = Annotated[
    SellerService,
    Depends(get_seller_service),
]

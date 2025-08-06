from typing import Annotated
from uuid import UUID

from fastapi import BackgroundTasks, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..db.async_engine_sqlmodel_postgres import get_session
from ..db.redis import is_jti_blacklisted
from ..db.sqlmodel_models import DeliveryPartner, Seller
from ..operations.o_delivery_partner import DeliveryPartnerService
from ..operations.o_sellerv2 import SellerService
from ..operations.o_shipment import ShipmentService
from ..operations.o_shipment_event import ShipmentEventService
from ..operations.o_shipmentv2 import ShipmentService as ShipmentServiceV2
from ..utils.token import (
    decode_access_token,
    oauth2_scheme_seller,
    oauth2_scheme_partner,
)

# Asynchronous database session dep annotation
SessionDep = Annotated[AsyncSession, Depends(get_session)]

# oauth2_scheme_seller = OAuth2PasswordBearer(tokenUrl="/seller/token")
# oauth2_scheme_partner = OAuth2PasswordBearer(tokenUrl="/partner/token")


# # Access token data dep
async def _get_access_token(token: str) -> dict:
    data = decode_access_token(token)

    if data is None or await is_jti_blacklisted(data["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
        )

    return data


# Seller access token data
async def get_seller_access_token(
    token: Annotated[str, Depends(oauth2_scheme_seller)],
) -> dict:
    return await _get_access_token(token)


# Delivery partner access token data
async def get_partner_access_token(
    token: Annotated[str, Depends(oauth2_scheme_partner)],
) -> dict:
    return await _get_access_token(token)


# Logged In Seller
# async def get_current_seller(
#     token_data: Annotated[dict, Depends(_get_access_token)],
#     session: SessionDep,
# ):
#     return await session.get(Seller, UUID(token_data["user"]["id"]))


async def get_current_seller(
    token_data: Annotated[dict, Depends(get_seller_access_token)],
    session: SessionDep,
):
    seller = await session.get(
        Seller,
        UUID(token_data["user"]["id"]),
    )

    if seller is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
        )

    return seller


# Logged In Delivery partner
async def get_current_partner(
    token_data: Annotated[dict, Depends(get_partner_access_token)],
    session: SessionDep,
):
    partner = await session.get(
        DeliveryPartner,
        UUID(token_data["user"]["id"]),
    )

    print(
        "=========== dependencies/get_current_partner",
        partner,
        UUID(token_data["user"]["id"]),
    )

    if partner is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
        )

    return partner


# Shipment service dep
# def get_shipment_service(session: SessionDep):
#     """
#     Defines a dependency function get_shipment_service that
#     takes an AsyncSession (via SessionDep) and returns a ShipmentService instance.

#     Components:

#     session: SessionDep:
#     The function expects an AsyncSession injected via SessionDep.
#     The Annotated type ensures FastAPI resolves get_session to provide the session.

#     ShipmentService: A custom service class (not shown but implied) that encapsulates
#     business logic for shipment operations (e.g., CRUD operations on the shipment table).

#     return ShipmentService(session):
#     Instantiates and returns a ShipmentService object,
#     passing the session to its constructor.

#     Purpose: Provides a service layer to abstract database operations,
#     promoting separation of concerns. The service likely handles queries like retrieving,
#     creating, or updating shipments.
#     """
#     return ShipmentService(session)


# Shipment service dep
def get_shipment_service(session: SessionDep):
    return ShipmentService(
        session, DeliveryPartnerService(session), ShipmentEventService(session)
    )


def get_shipment_service_v2(session: SessionDep, tasks: BackgroundTasks):
    return ShipmentServiceV2(
        session,
        DeliveryPartnerService(session),
        ShipmentEventService(session, tasks),
    )


# Seller service dep
def get_seller_service(session: SessionDep, tasks: BackgroundTasks):
    return SellerService(session, tasks)


# Delivery partner service dep
def get_delivery_partner_service(session: SessionDep, tasks: BackgroundTasks):
    return DeliveryPartnerService(session, tasks)


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


ServiceDepV2 = Annotated[
    ShipmentServiceV2,
    Depends(get_shipment_service_v2),
]

SellerDep = Annotated[Seller, Depends(get_current_seller)]


# Delivery partner dep annotation
DeliveryPartnerDep = Annotated[
    DeliveryPartner,
    Depends(get_current_partner),
]


# Shipment service dep annotation
ShipmentServiceDep = Annotated[
    ShipmentService,
    Depends(get_shipment_service),
]

ShipmentServiceDepV2 = Annotated[
    ShipmentServiceV2,
    Depends(get_shipment_service_v2),
]

# Seller service dep annotation
SellerServiceDep = Annotated[
    SellerService,
    Depends(get_seller_service),
]

# Delivery partner service dep annotaion
DeliveryPartnerServiceDep = Annotated[
    DeliveryPartnerService,
    Depends(get_delivery_partner_service),
]

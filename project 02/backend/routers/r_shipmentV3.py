from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Body, HTTPException, Path, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..db.async_engine_sqlmodel_postgres import SessionDep
from ..db.sqlmodel_models import Shipment
from ..operations.o_delivery_partner import DeliveryPartnerService
from ..operations.o_shipment_event import ShipmentEventService
from ..operations.o_shipmentv2 import ShipmentService
from ..routers.dependencies import SellerDep, ServiceDepV2, ShipmentServiceDepV2
from ..schemas.s_schemas import (
    ShipmentCreate,
    ShipmentRead,
    ShipmentStatus,
    ShipmentUpdate,
)

router = APIRouter()


##  a shipment by id
@router.get("/", response_model=ShipmentRead)
# async def get_shipment(id: int,  service: ServiceDep):
async def get_shipment(id: UUID, seller: SellerDep, service: SessionDep):

    partner_service = DeliveryPartnerService(session=service)
    event_service = ShipmentEventService(session=service)

    shipment = await ShipmentService(
        service, partner_service=partner_service, event_service=event_service
    ).get(id)
    # shipment = await service.get(id)
    # Check for shipment with given id
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )

    return shipment


# @router.get("/v2", response_model=ShipmentRead)
# # async def get_shipment(id: int,  service: ServiceDep):
# async def get_shipmentv2(id: UUID, service: ServiceDep):

#     # shipment = ShipmentService(service).get(id)
#     shipment = await service.get(id)
#     # Check for shipment with given id
#     if shipment is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Given id doesn't exist!",
#         )


#     return shipment
@router.get("/v2/", response_model=ShipmentRead)
# async def get_shipment(id: int,  service: ServiceDep):
async def get_shipmentv2(id: UUID, service: ShipmentServiceDepV2):

    # shipment = ShipmentService(service).get(id)
    shipment = await service.get(id)
    # Check for shipment with given id
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )

    return shipment


### Create a new shipment with content and weight
@router.post("/")
async def submit_shipment(
    seller: SellerDep,
    shipment: ShipmentCreate,
    service: SessionDep,
):
    """
    why we dont use below sentence and we face an error:
        # return await ShipmentService(service).add(shipment)

    Instead of calling service.add(shipment) directly, it creates a new ShipmentService instance with ShipmentService(service).
    """
    # return await service.add(shipment)
    partner_service = DeliveryPartnerService(
        session=service
    )  # Instantiate DeliveryPartnerService
    event_service = ShipmentEventService(
        session=service
    )  # Instantiate ShipmentEventService
    return await ShipmentService(
        service, partner_service=partner_service, event_service=event_service
    ).add(shipment, seller)


@router.post("/v2/")
async def submit_shipmentv3(
    seller: SellerDep, shipment: ShipmentCreate, service: ShipmentServiceDepV2
) -> Shipment:
    """
    Both functions with name submit_shipment & submit_shipmentv2 has a same result
    with different dependencies
    """
    return await service.add(shipment, seller)
    # return await ShipmentService(service).add(shipment)


### Update fields of a shipment
@router.patch("/", response_model=ShipmentRead)
async def update_shipment(
    id: UUID, shipment_update: ShipmentUpdate, service: SessionDep
):
    partner_service = DeliveryPartnerService(session=service)
    event_service = ShipmentEventService(session=service)

    # Update data with given fields
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update",
        )

    shipment = await ShipmentService(
        service, partner_service=partner_service, event_service=event_service
    ).update(id, update)

    return shipment


### Update fields of a shipment
@router.patch("/v2", response_model=ShipmentRead)
async def update_shipmentv2(
    id: UUID,
    shipment_update: ShipmentUpdate,
    service: ShipmentServiceDepV2,
):
    # Update data with  only given fields
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update",
        )

    shipment = await service.update(id, update)
    # shipment = await ShipmentService(service).update(id, update)

    return shipment


### Cancel a shipment by id
@router.get("/cancel")
async def cancel_shipment(
    id: UUID,
    service: SessionDep,
    seller: SellerDep,
) -> Shipment:

    partner_service = DeliveryPartnerService(session=service)
    event_service = ShipmentEventService(session=service)

    return await ShipmentService(
        service, partner_service=partner_service, event_service=event_service
    ).cancel(id, seller)


### cancel a shipment by id
@router.get("/cancel/v2", response_model=ShipmentRead)
async def cancel_shipmentv2(
    id: UUID,
    seller: SellerDep,
    service: ShipmentServiceDepV2,
) -> Shipment:

    return await service.cancel(id, seller)


# ### Delete a shipment by id
# @router.delete("/")
# async def delete_shipment(id: UUID, service: SessionDep) -> dict[str, str]:
#     # Remove from database
#     partner_service = DeliveryPartnerService(service)
#     await ShipmentService(service, partner_service).delete(id)

#     return {"detail": f"Shipment with id #{id} is deleted!"}


# ### Delete a shipment by id
# @router.delete("/v2")
# async def delete_shipmentv2(id: UUID, service: ShipmentServiceDepV2) -> dict[str, str]:
#     # Remove from database
#     await service.delete(id)
#     # await ShipmentService(service).delete(id)

#     return {"detail": f"Shipment with id #{id} is deleted!"}

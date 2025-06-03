from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Path, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..db.async_engine_sqlmodel_postgres import SessionDep
from ..db.sqlmodel_models import Shipment
from ..operations.o_shipment import ShipmentService
from ..routers.dependencies import ServiceDep
from ..schemas.s_schemas import (
    ShipmentCreate,
    ShipmentRead,
    ShipmentStatus,
    ShipmentUpdate,
)

router = APIRouter()


###  a shipment by id
@router.get("/", response_model=ShipmentRead)
# async def get_shipment(id: int,  service: ServiceDep):
async def get_shipment(id: int, service: SessionDep):

    shipment = await ShipmentService(service).get(id)
    # shipment = await service.get(id)
    # Check for shipment with given id
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )

    return shipment


@router.get("/v2", response_model=ShipmentRead)
# async def get_shipment(id: int,  service: ServiceDep):
async def get_shipmentv2(id: int, service: ServiceDep):

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
async def submit_shipment(shipment: ShipmentCreate, service: SessionDep) -> Shipment:
    """
    why we dont use below sentence and we face an error:
        # return await ShipmentService(service).add(shipment)

    Instead of calling service.add(shipment) directly, it creates a new ShipmentService instance with ShipmentService(service).
    """
    # return await service.add(shipment)
    return await ShipmentService(service).add(shipment)


@router.post("/v2/")
async def submit_shipmentv2(shipment: ShipmentCreate, service: ServiceDep) -> Shipment:
    """
    Both functions with name submit_shipment & submit_shipmentv2 has a same result
    with different dependencies
    """
    return await service.add(shipment)
    # return await ShipmentService(service).add(shipment)


### Update fields of a shipment
@router.patch("/", response_model=ShipmentRead)
async def update_shipment(
    id: int, shipment_update: ShipmentUpdate, service: SessionDep
):
    # Update data with given fields
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update",
        )

    shipment = await ShipmentService(service).update(id, update)

    return shipment


### Update fields of a shipment
@router.patch("/v2", response_model=ShipmentRead)
async def update_shipmentv2(
    id: int, shipment_update: ShipmentUpdate, service: ServiceDep
):
    # Update data with given fields
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update",
        )

    shipment = await service.update(id, update)
    # shipment = await ShipmentService(service).update(id, update)

    return shipment


### Delete a shipment by id
@router.delete("/")
async def delete_shipment(id: int, service: SessionDep) -> dict[str, str]:
    # Remove from database
    await ShipmentService(service).delete(id)

    return {"detail": f"Shipment with id #{id} is deleted!"}


### Delete a shipment by id
@router.delete("/v2")
async def delete_shipmentv2(id: int, service: ServiceDep) -> dict[str, str]:
    # Remove from database
    await service.delete(id)
    # await ShipmentService(service).delete(id)

    return {"detail": f"Shipment with id #{id} is deleted!"}

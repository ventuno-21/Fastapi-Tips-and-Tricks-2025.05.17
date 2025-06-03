from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Path, Query
from pydantic import BaseModel, Field
from starlette import status

from ..db.sqlmodel_models import Shipment
from ..db.async_engine_sqlmodel_postgres import SessionDep
from ..schemas.s_schemas import (
    ShipmentCreate,
    ShipmentRead,
    ShipmentStatus,
    ShipmentUpdate,
)

router = APIRouter()


###  a shipment by id
@router.get("/", response_model=ShipmentRead)
def get_shipment(id: int, session: SessionDep):

    shipment = session.get(Shipment, id)
    # Check for shipment with given id
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )

    return shipment


### Create a new shipment with content and weight
@router.post("/", response_model=None)
def submit_shipment(shipment: ShipmentCreate, session: SessionDep) -> dict[str, int]:
    new_shipment = Shipment(
        **shipment.model_dump(),
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=3),
    )
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)

    return {"id": new_shipment.id}


### Update fields of a shipment
@router.patch("/", response_model=ShipmentRead)
def update_shipment(id: int, shipment_update: ShipmentUpdate, session: SessionDep):
    # Update data with given fields
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update",
        )

    shipment = session.get(Shipment, id)
    shipment.sqlmodel_update(update)

    session.add(shipment)
    session.commit()
    session.refresh(shipment)

    return shipment


### Delete a shipment by id
@router.delete("/")
def delete_shipment(id: int, session: SessionDep) -> dict[str, str]:
    # Remove from database
    session.delete(session.get(Shipment, id))
    session.commit()

    return {"detail": f"Shipment with id #{id} is deleted!"}

from fastapi import APIRouter, Body, Path, Query, HTTPException
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from starlette import status
from ..db.sync_engine_sqlite import Database
from ..schemas.s_schemas import (
    ShipmentRead,
    ShipmentCreate,
    ShipmentStatus,
    ShipmentUpdate,
)

router = APIRouter()

db = Database()


###  a shipment by id
@router.get("/", response_model=ShipmentRead)
def get_shipment(id: int):
    shipment = db.get(id)
    # Check for shipment with given id
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )

    return shipment


### Create a new shipment with content and weight
@router.post("/", response_model=None)
def submit_shipment(shipment: ShipmentCreate) -> dict[str, int]:
    new_id = db.create(shipment)
    return {"id": new_id}


### Update fields of a shipment
@router.patch("/", response_model=ShipmentRead)
def update_shipment(id: int, shipment: ShipmentUpdate):
    db.update(id, shipment)
    return shipment


### Delete a shipment by id
@router.delete("/")
def delete_shipment(id: int) -> dict[str, str]:
    db.delete(id)
    return {"detail": f"Shipment with id #{id} is deleted!"}

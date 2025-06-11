from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Path, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..db.async_engine_sqlmodel_postgres import SessionDep
from ..db.sqlmodel_models import Seller, Shipment
from ..schemas.s_schemas import (
    ShipmentCreate,
    ShipmentRead,
    ShipmentStatus,
    ShipmentUpdate,
)


class ShipmentService:
    def __init__(self, session: AsyncSession):
        # Get database session to perform database operations
        self.session = session

    # Get a shipment by id
    async def get(self, id: int) -> Shipment:
        return await self.session.get(Shipment, id)

    # Add a new shipment
    async def add(self, shipment_create: ShipmentCreate, seller: Seller) -> Shipment:

        print("+" * 50)
        print(shipment_create.model_dump())

        data = shipment_create.model_dump()
        data.pop("status", None)  # remove if present
        data.pop("estimated_delivery", None)  # remove if present

        new_shipment = Shipment(
            **data,
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now() + timedelta(days=3),
            seller_id=seller.id
        )
        self.session.add(new_shipment)
        await self.session.commit()
        await self.session.refresh(new_shipment)

        return new_shipment

    # Update an existing shipment
    async def update(self, id: int, shipment_update: dict) -> Shipment:
        shipment = await self.get(id)
        shipment.sqlmodel_update(shipment_update)

        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)

        return shipment

    # Delete a shipment
    async def delete(self, id: int) -> None:
        await self.session.delete(await self.get(id))
        await self.session.commit()

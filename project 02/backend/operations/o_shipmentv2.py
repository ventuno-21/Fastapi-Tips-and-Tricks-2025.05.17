from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Body, HTTPException, Path, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..utils.token import decode_url_safe_token

from ..db.async_engine_sqlmodel_postgres import SessionDep
from ..db.sqlmodel_models import DeliveryPartner, Seller, Shipment, Review
from ..schemas.s_schemas import (
    ShipmentCreate,
    ShipmentRead,
    ShipmentStatus,
    ShipmentUpdate,
)
from .o_base import BaseService
from .o_delivery_partner import DeliveryPartnerService
from .o_shipment_event import ShipmentEventService


class ShipmentService(BaseService):
    def __init__(
        self,
        session: AsyncSession,
        partner_service: DeliveryPartnerService,
        event_service: ShipmentEventService,
    ):
        super().__init__(Shipment, session)
        self.partner_service = partner_service
        self.event_service = event_service

    # Get a shipment by id
    async def get(self, id: UUID) -> Shipment | None:
        return await self._get(id)

    # Add a new shipment
    async def add(self, shipment_create: ShipmentCreate, seller: Seller) -> Shipment:
        print("*" * 50)
        print(shipment_create)
        print(shipment_create.model_dump())
        print(seller)
        print(seller.id)
        print("*" * 50)
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now() + timedelta(days=3),
            seller_id=seller.id,
        )
        print("new_shipment===============>   ", new_shipment)

        # Assign delivery partner to the shipment
        partner = await self.partner_service.assign_shipment(
            new_shipment,
        )
        # Add the delivery partner foreign key
        new_shipment.delivery_partner_id = partner.id

        shipment = await self._add(new_shipment)

        event = await self.event_service.add(
            shipment=shipment,
            location=seller.zip_code,
            status=ShipmentStatus.placed,
            description=f"assigned to {partner.name}",
        )

        shipment.timeline.append(event)

        return shipment

    # Update an existing shipment
    async def update(
        self,
        id: UUID,
        shipment_update: ShipmentUpdate,
        partner: DeliveryPartner,
    ) -> Shipment:
        shipment = await self.get(id)

        if shipment.delivery_partner_id != partner.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized (add: o_shipmentv2/update)",
            )

        update = shipment_update.model_dump(exclude_none=True)

        if shipment_update.estimated_delivery:
            shipment.estimated_delivery = shipment_update.estimated_delivery

        if len(update) > 1 or not shipment_update.estimated_delivery:
            await self.event_service.add(
                shipment=shipment,
                **update,
            )
        return await self._update(shipment)

    async def rate(self, token: str, rating: int, comment: str):
        token_data = decode_url_safe_token(token)

        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized",
            )

        shipment = await self.get(UUID(token_data["id"]))

        new_review = Review(
            rating=rating,
            comment=comment if comment else None,
            shipment_id=shipment.id,
        )

        self.session.add(new_review)
        await self.session.commit()

    async def cancel(self, id: UUID, seller: Seller) -> Shipment:
        shipment = await self.get(id)

        if shipment.seller_id != seller.id:
            raise HTTPException(
                status=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized (add: o_shipmentv2/shipmentService/cancel)",
            )
        event = await self.event_service.add(
            shipment=shipment, status=ShipmentStatus.cancelled
        )

        shipment.timeline.append(event)

        return shipment

    # Delete a shipment
    async def delete(self, id: UUID) -> None:
        await self._delete(await self.get(id))

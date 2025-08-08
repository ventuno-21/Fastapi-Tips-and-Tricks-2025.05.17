import os
from datetime import datetime, timedelta
from enum import Enum
from typing import Annotated, Optional
from uuid import UUID

from dotenv import load_dotenv
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Body,
    Form,
    HTTPException,
    Path,
    Query,
    Request,
)
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..db.async_engine_sqlmodel_postgres import SessionDep
from ..db.sqlmodel_models import Shipment
from ..operations.o_delivery_partner import DeliveryPartnerService
from ..operations.o_shipment_event import ShipmentEventService
from ..operations.o_shipmentv2 import ShipmentService
from ..routers.dependencies import (
    DeliveryPartnerDep,
    SellerDep,
    ServiceDepV2,
    ShipmentServiceDep,
    ShipmentServiceDepV2,
)
from ..schemas.s_schemas import (
    ShipmentCreate,
    ShipmentRead,
    ShipmentStatus,
    ShipmentUpdate,
)
from ..utils.mail import TEMPLATE_DIR


router = APIRouter()

load_dotenv()
APP_DOMAIN = os.getenv("APP_DOMAIN")

templates = Jinja2Templates(TEMPLATE_DIR)


### Tracking details of shipment
@router.get("/track")
async def get_tracking(request: Request, id: UUID, service: ShipmentServiceDepV2):
    # Check for shipment with given id
    shipment = await service.get(id)

    context = shipment.model_dump()
    context["status"] = shipment.status
    context["partner"] = shipment.delivery_partner.name
    context["timeline"] = shipment.timeline
    # modifying the list in place, flipping the order
    context["timeline"].reverse()

    return templates.TemplateResponse(
        request=request,
        name="email/track.html",
        context=context,
    )


##  a shipment by id
@router.get("/", response_model=ShipmentRead)
# async def get_shipment(id: int,  service: ServiceDep):
async def get_shipment(
    id: UUID, seller: SellerDep, service: SessionDep, tasks: BackgroundTasks
):

    partner_service = DeliveryPartnerService(session=service, tasks=tasks)
    event_service = ShipmentEventService(session=service, tasks=tasks)

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
    tasks: BackgroundTasks,
):
    """
    why we dont use below sentence and we face an error:
        # return await ShipmentService(service).add(shipment)

    Instead of calling service.add(shipment) directly, it creates a new ShipmentService instance with ShipmentService(service).
    """
    # return await service.add(shipment)
    partner_service = DeliveryPartnerService(
        session=service, tasks=tasks
    )  # Instantiate DeliveryPartnerService
    event_service = ShipmentEventService(session=service, tasks=tasks)

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
    id: UUID,
    shipment_update: ShipmentUpdate,
    service: SessionDep,
    tasks: BackgroundTasks,
    partner: DeliveryPartnerDep,
):
    partner_service = DeliveryPartnerService(session=service)
    event_service = ShipmentEventService(session=service, tasks=tasks)

    # Update data with given fields
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update",
        )

    shipment = await ShipmentService(
        service, partner_service=partner_service, event_service=event_service
    ).update(id, shipment_update, partner)

    return shipment


### Update fields of a shipment
@router.patch("/v2", response_model=ShipmentRead)
async def update_shipmentv2(
    id: UUID,
    shipment_update: ShipmentUpdate,
    partner: DeliveryPartnerDep,
    service: ShipmentServiceDepV2,
):
    # Update data with  only given fields
    update = shipment_update.model_dump(exclude_none=True)
    print(f"update type ============================ {type(update)}")
    print(f"shipment_update type ============================ {type(shipment_update)}")

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update",
        )

    shipment = await service.update(id, shipment_update, partner)
    # shipment = await ShipmentService(service).update(id, update)

    return shipment


### Cancel a shipment by id
@router.get("/cancel")
async def cancel_shipment(
    id: UUID,
    service: SessionDep,
    seller: SellerDep,
) -> Shipment:

    partner_service = DeliveryPartnerService(session=service, tasks=BackgroundTasks)
    event_service = ShipmentEventService(session=service, tasks=BackgroundTasks)

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


### Sumbit a reivew for a shipment
@router.get("/review")
async def submit_review_page(request: Request, token: str):
    return templates.TemplateResponse(
        request=request,
        name="review.html",
        context={
            "review_url": f"http://{APP_DOMAIN}/shipmentv3/review?token={token}",
        },
    )


### Sumbit a reivew for a shipment
@router.post("/review")
async def submit_review(
    token: str,
    rating: Annotated[int, Form(ge=1, le=5)],
    comment: Annotated[str | None, Form()],
    service: ShipmentServiceDepV2,
):
    await service.rate(token, rating, comment)
    return {"detail": "Review submitted"}

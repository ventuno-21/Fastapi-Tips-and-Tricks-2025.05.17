from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ..db.redis import add_jti_to_blacklist
from ..schemas.s_delivery_partner import (
    DeliveryPartnerCreate,
    DeliveryPartnerRead,
    DeliveryPartnerUpdate,
)
from ..utils.token import oauth2_scheme_partner
from .dependencies import (
    DeliveryPartnerDep,
    DeliveryPartnerServiceDep,
    get_partner_access_token,
)

# oauth2_scheme_partner = OAuth2PasswordBearer(tokenUrl="/partner/token")

router = APIRouter(tags=["Delivery Partner"])


### Register a new delivery partner
@router.post("/signup", response_model=DeliveryPartnerRead)
async def register_delivery_partner(
    partner: DeliveryPartnerCreate,
    service: DeliveryPartnerServiceDep,
):
    return await service.add(partner)


### Login a delivery partner
@router.post("/token")
async def login_delivery_partner(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: DeliveryPartnerServiceDep,
):
    token = await service.token(request_form.username, request_form.password)
    return {
        "access_token": token,
        "type": "bearer",
    }


### Verify Delivery Partner Email
@router.get("/verify")
async def verify_delivery_partner_email(
    token: str,
    service: DeliveryPartnerServiceDep,
):
    await service.verify_email(token)
    return {"detail": "Account verified"}


### Update the logged in delivery partner
# @router.post("/update", response_model=DeliveryPartnerRead)
@router.post(
    "/update",
    response_model=DeliveryPartnerRead,
    tags=["Delivery Partner"],
)
async def update_delivery_partner(
    partner_update: DeliveryPartnerUpdate,
    partner: DeliveryPartnerDep,
    service: DeliveryPartnerServiceDep,
    token: Annotated[str, Security(oauth2_scheme_partner)],
    # This is how security gets applied
):
    """
    Update data with given fields
    uses Pydantic’s model_dump() method to convert the partner_update object
    (likely a BaseModel) into a plain Python dict. The key part is:

    exclude_none=True — What It Does?
    It tells Pydantic to exclude any fields where the value is None from the
    output dictionary.
    """
    update = partner_update.model_dump(exclude_none=True)
    print(" ++++++++++++++++++++++++++++ what got updated ==> ", update)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update",
        )
    print(" ***************   Inside update delivery partner router *********")

    return await service.update(
        partner.sqlmodel_update(update),
    )


### Logout a delivery partner
@router.get("/logout")
async def logout_delivery_partner(
    # token_data: Annotated[dict, Depends(get_partner_access_token)],
    token_data: Annotated[dict, Security(get_partner_access_token)],
):
    await add_jti_to_blacklist(token_data["jti"])
    return {"detail": "Successfully logged out"}

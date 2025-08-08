import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Form, HTTPException, Security, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import EmailStr
from fastapi.templating import Jinja2Templates

from ..utils.mail import TEMPLATE_DIR

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
load_dotenv()
APP_DOMAIN = os.getenv("APP_DOMAIN")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/seller/token")

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


### Email Password Reset Link
@router.get("/forgot_password")
async def forgot_password(email: EmailStr, service: DeliveryPartnerServiceDep):
    await service.send_password_reset_link(email, router_prefix="/partner")
    return {"detail": "Check email for password reset link"}


### Password Reset Form
@router.get("/reset_password_form")
async def get_reset_password_form(request: Request, token: str):
    router_prefix = "/partner"
    templates = Jinja2Templates(TEMPLATE_DIR)

    return templates.TemplateResponse(
        request=request,
        name="password/reset_password_form.html",
        context={
            "reset_url": f"http://{APP_DOMAIN}{router_prefix}/reset_password?token={token}"
        },
    )


### Reset Seller Password
@router.post("/reset_password")
async def reset_password(
    request: Request,
    token: str,
    password: Annotated[str, Form()],
    service: DeliveryPartnerServiceDep,
):
    is_success = await service.reset_password(token, password)

    templates = Jinja2Templates(TEMPLATE_DIR)
    return templates.TemplateResponse(
        request=request,
        name=(
            "password/reset_password_success.html"
            if is_success
            else "password/reset_password_failed.html"
        ),
    )


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

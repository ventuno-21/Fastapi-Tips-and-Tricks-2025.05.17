import os
from datetime import datetime, timedelta
from enum import Enum
from typing import Annotated, Optional

from dotenv import load_dotenv
from fastapi import APIRouter, Body, Depends, Form, HTTPException, Path, Query, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..db.async_engine_sqlmodel_postgres import SessionDep
from ..db.redis import add_jti_to_blacklist, is_jti_blacklisted
from ..db.sqlmodel_models import Seller, Shipment
from ..operations.o_shipment import ShipmentService
from ..routers.dependencies import SellerServiceDep
from ..schemas.s_seller import SellerCreate, SellerRead
from ..utils.mail import TEMPLATE_DIR
from ..utils.token import decode_access_token
from .dependencies import _get_access_token, get_current_seller, get_seller_access_token

load_dotenv()
APP_DOMAIN = os.getenv("APP_DOMAIN")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/seller/token")

router = APIRouter()


### Register a seller
@router.post("/signup", response_model=SellerRead)
async def register_seller(seller: SellerCreate, service: SellerServiceDep):
    return await service.add(seller)


### Login the seller
@router.post("/token")
async def login_seller(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: SellerServiceDep,
):
    token = await service.token(request_form.username, request_form.password)
    return {
        "access_token": token,
        "type": "jwt",
    }


### Verify Seller Email
@router.get("/verify")
async def verify_seller_email(token: str, service: SellerServiceDep):
    await service.verify_email(token)
    return {"detail": "Account verified"}


### Email Password Reset Link
@router.get("/forgot_password")
async def forgot_password(email: EmailStr, service: SellerServiceDep):
    await service.send_password_reset_link(email, router_prefix="/seller")
    return {"detail": "Check email for password reset link"}


### Password Reset Form
@router.get("/reset_password_form")
async def get_reset_password_form(request: Request, token: str):
    router_prefix = "/seller"
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
    service: SellerServiceDep,
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


@router.get("/dashboard")
async def get_dashboard(
    session: SessionDep,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    """
    Now dashboard will be token authenticated
    """

    data = decode_access_token(token)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )

    seller = await session.get(Seller, data["user"]["id"])
    return {"seller": seller}


### Logout a seller
@router.get("/logout")
async def logout_seller(
    token_data: Annotated[dict, Depends(get_seller_access_token)],
):
    await add_jti_to_blacklist(token_data["jti"])
    return {"detail": "Successfully logged out"}


@router.get("/dashboardv2")
async def get_dashboardv2(
    session: SessionDep, user: Annotated[Seller, Depends(get_current_seller)]
):
    """
    Now dashboard will be token authenticated

    """
    print("&" * 40)
    print(user)
    seller = await session.get(Seller, user.id)
    return {"seller": seller}

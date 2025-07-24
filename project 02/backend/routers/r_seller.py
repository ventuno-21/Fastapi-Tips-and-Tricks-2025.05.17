from datetime import datetime, timedelta
from enum import Enum
from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..db.async_engine_sqlmodel_postgres import SessionDep
from ..db.redis import add_jti_to_blacklist, is_jti_blacklisted
from ..db.sqlmodel_models import Seller, Shipment
from ..operations.o_shipment import ShipmentService
from ..routers.dependencies import SellerServiceDep
from ..schemas.s_seller import SellerCreate, SellerRead
from ..utils.token import decode_access_token
from .dependencies import _get_access_token, get_seller_access_token, get_current_seller

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

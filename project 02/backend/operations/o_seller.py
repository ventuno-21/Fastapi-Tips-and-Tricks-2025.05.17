from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Path, Query
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..db.async_engine_sqlmodel_postgres import SessionDep
from ..db.sqlmodel_models import Seller
from ..schemas.s_seller import SellerCreate
from ..utils.token import generate_access_token

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SellerService:
    def __init__(self, session: AsyncSession):
        # Get database session to perform database operations
        self.session = session

    async def add(self, credentials: SellerCreate) -> Seller:
        seller = Seller(
            **credentials.model_dump(exclude=["password"]),
            # Hashed password
            password_hash=password_context.hash(credentials.password),
        )
        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)

        return seller

    async def token(self, email, password) -> str:
        # Validate the credentials
        result = await self.session.execute(select(Seller).where(Seller.email == email))
        """
            The line seller = result.scalar() assigns the first Seller object
            (or None) from the query result to the variable seller.
            Since the query select(Seller).where(Seller.email == email) is 
            filtering for a Seller record with a specific email, 
            .scalar() is used to get the matching Seller object (if it exists)
            or None (if no seller with that email is found).
            This is typically used when you expect at most one result
            (e.g., looking up a user by a unique field like email).
        """
        seller = result.scalar()

        print(f" ******* Difference between result and result scalar *******")
        print(f" result = {result}")
        print(f" result.scalar() = {seller}")
        print("*" * 30)

        if seller is None or not password_context.verify(
            password,
            seller.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email or password is incorrect",
            )

        token = generate_access_token(
            data={
                "user": {
                    "name": seller.name,
                    "id": str(seller.id),
                }
            }
        )

        return token

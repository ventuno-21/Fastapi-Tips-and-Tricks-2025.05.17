import os
from uuid import UUID

from dotenv import load_dotenv
from fastapi import BackgroundTasks, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.sqlmodel_models import User
from ..utils.token import (
    decode_url_safe_token,
    generate_access_token,
    generate_url_safe_token,
)
from .o_base import BaseService
from .o_notification import NotificationService

load_dotenv()
APP_DOMAIN = os.getenv("APP_DOMAIN")

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService(BaseService):
    def __init__(self, model: User, session: AsyncSession, tasks: BackgroundTasks):
        self.model = model
        self.session = session
        self.notification_service = NotificationService(tasks)

    async def _add_user(self, data: dict, router_prefix: str) -> User:
        user = self.model(
            **data,
            password_hash=password_context.hash(data["password"]),
        )
        # Add the user to database and get refreshed data
        user = await self._add(user)
        # Generate the token with user id
        token = generate_url_safe_token(
            {
                # Email can be skipped as not used in our case
                # "email": user.email,
                "id": str(user.id)
            }
        )
        # Send registration email with verification link
        await self.notification_service.send_email_with_template(
            recipients=[user.email],
            subject="Verify Your Account With Ventuno",
            context={
                "username": user.name,
                "verification_url": f"http://{APP_DOMAIN}/{router_prefix}/verify?token={token}",
            },
            template_name="email/mail_verification.html",
        )

        return user

    async def verify_email(self, token: str):
        token_data = decode_url_safe_token(token)
        # Validate the token
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
            )
        # Update the verified field on the user
        # to mark user as verified
        user = await self._get(UUID(token_data["id"]))
        user.email_verified = True

        await self._update(user)

    async def _get_by_email(self, email) -> User | None:
        # result = self.session.execute(self.model).where(self.model.email == email)
        # seller=result.scalar()

        return await self.session.scalar(
            select(self.model).where(self.model.email == email)
        )

    async def _generate_token(self, email, password) -> str:
        # Validate the credentials
        user = await self._get_by_email(email)

        if user is None or not password_context.verify(
            password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email or password is incorrect",
            )

        if not user.email_verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Your email is not verified",
            )

        return generate_access_token(
            data={
                "user": {
                    "name": user.name,
                    "id": str(user.id),
                },
            }
        )

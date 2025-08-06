import os
from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import uuid4

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

# Load environment variables from .env file
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


_serializer = URLSafeTimedSerializer(secret_key=SECRET_KEY)


oauth2_scheme_seller = OAuth2PasswordBearer(tokenUrl="/seller/token")
oauth2_scheme_partner = OAuth2PasswordBearer(tokenUrl="/partner/token")


def generate_access_token(
    data: dict,
    expiry: timedelta = timedelta(minutes=90),
    # expiry: timedelta = timedelta(days=7),
) -> str:
    return jwt.encode(
        payload={
            **data,
            "jti": str(uuid4()),
            "exp": datetime.now(timezone.utc) + expiry,
        },
        algorithm=ALGORITHM,
        key=SECRET_KEY,
    )


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            jwt=token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Expired token , {e}",
        )

    except jwt.PyJWTError:
        return None


# If we dont want to use OAuth2PasswordBearer, we can also access to token like below therough HTTPBearer
class AccessTokenBearer(HTTPBearer):
    async def __call__(self, request):
        # request.headers.get("Authorization").split(" ")[1]
        auth_credentials = await super().__call__(request)
        token = auth_credentials.credentials
        token_data = decode_access_token(token)
        if token_data is None:
            raise HTTPException(status_code=401, detail="Not authorized")

        return token_data


access_token_bearer = AccessTokenBearer()

another_way_to_access_token = Annotated[dict, Depends(access_token_bearer)]


def generate_url_safe_token(data: dict) -> str:
    return _serializer.dumps(data)


def decode_url_safe_token(token: str, expiry: timedelta | None = None) -> dict | None:
    try:
        return _serializer.loads(
            token,
            max_age=expiry.total_seconds() if expiry else None,
        )
    except (BadSignature, SignatureExpired):
        return None

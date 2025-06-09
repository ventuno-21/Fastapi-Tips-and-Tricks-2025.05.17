import os
from datetime import datetime, timedelta, timezone
from uuid import uuid4
import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from typing import Annotated

# Load environment variables from .env file
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def generate_access_token(
    data: dict,
    expiry: timedelta = timedelta(minutes=1),
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

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import Annotated
from db.sync_engine import get_db
from db.models import Todos, Users
from starlette import status
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import timedelta, datetime, timezone

router = APIRouter()

db_dependancy = Annotated[Session, Depends(get_db)]

# bcrypt_context = CryptContext(schemes=["bcrypt"], depracated="auto")
bcrypt_context = CryptContext(schemes=["bcrypt"])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
SECRET_KEY = "IUIBUDY*&^*&%DF%D^&CGDHCBDCHKCHYUID^C&D*CYDCDBCMDKKDGCKDGHG"
ALGORITHM = "HS256"


class CreateUserRequest(BaseModel):
    username: str
    email: str
    firstname: str
    lastname: str
    password: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hash_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):

    expires = datetime.now(timezone.utc) + timedelta(minutes=34)
    encode_items = {"id": user_id, "username": username, "exp": expires}
    return jwt.encode(encode_items, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    """
    "oauth2_bearer" will call "login_for_access_token" function because in
    above we mention the link of  "login_for_access_token" function:

    ===> oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

    please be aware that "login_for_access_token" function have to return
    below dictionary:

    ===> return {"access_token": token, "token_type": "bearer"}

    Otherwise we can not access to "token"
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate a user",
            )
        else:
            return {"username": username, "id": user_id}
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate a user, Detail: {e}",
        )


@router.get("/")
async def all_users(db: db_dependancy):
    return db.query(Users).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependancy, create_user_requestt: CreateUserRequest):
    user = Users(
        firstname=create_user_requestt.firstname,
        username=create_user_requestt.username,
        email=create_user_requestt.email,
        lastname=create_user_requestt.lastname,
        hash_password=bcrypt_context.hash(create_user_requestt.password),
        role=create_user_requestt.role,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependancy,
):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate a user",
        )
    else:
        token = create_access_token(user.username, user.id, timedelta(minutes=20))
        """
            The response of the token endpoint must be a JSON object.

            It should have a token_type. In our case, as we are using "Bearer" tokens, 
            the token type should be "bearer".

            And it should have an access_token, with a string containing our access token.
        """
        return {"access_token": token, "token_type": "bearer"}

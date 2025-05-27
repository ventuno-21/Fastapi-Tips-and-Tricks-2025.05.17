from fastapi import APIRouter, Depends, HTTPException, Path, Request, Response, Form
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from db.sync_engine import get_db
from db.models import Todos, Users
from starlette import status
from starlette.responses import RedirectResponse
from pydantic import BaseModel, ConfigDict, Field
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import timedelta, datetime, timezone
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

db_dependancy = Annotated[Session, Depends(get_db)]

# bcrypt_context = CryptContext(schemes=["bcrypt"], depracated="auto")
bcrypt_context = CryptContext(schemes=["bcrypt"])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth2/token")
SECRET_KEY = "IUIBUDY*&^*&%DF%D^&CGDHCBDCHKCHYUID^C&D*CYDCDBCMDKKDGCKDGHG"
ALGORITHM = "HS256"
templates = Jinja2Templates(directory="templates")


# Define a class to handle and parse the login form data from the request
class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request  # Store the incoming request
        self.username: Optional[str] = (
            None  # Placeholder for extracted username (email)
        )
        self.password: Optional[str] = None  # Placeholder for extracted password

    # Async method to extract form data from the POST request
    async def create_oauth_form(self):
        form = await self.request.form()  # Await form data extraction
        self.username = form.get("email")  # Get email input from form
        self.password = form.get("password")  # Get password input from form


# Handle GET request to display the login page
@router.get("/", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse(
        "login.html", {"request": request}
    )  # Render login page


# Handle POST request to authenticate user login
@router.post("/", response_class=HTMLResponse)
async def login_post(db: db_dependancy, request: Request):
    try:
        # Instantiate and parse form data
        form = LoginForm(request)
        await form.create_oauth_form()

        # Create a response object to allow setting cookies or redirect
        response = RedirectResponse(url="/todo", status_code=status.HTTP_302_FOUND)

        # Call a function to validate the user's credentials and set authentication cookies
        validate_user_cookie = await login_for_access_token(
            response=response, form_data=form, db=db
        )

        # If validation fails, show the login page again with an error message
        if not validate_user_cookie:
            msg = "Incorrect Username or Password"
            return templates.TemplateResponse(
                "login.html", {"request": request, "msg": msg}
            )

        # If successful, redirect to the /todo page
        return response

    except Exception as e:
        # Log the exception (for debugging) and show a generic error message
        print(f"Login error: {e}")
        msg = "Unknown Error"
        return templates.TemplateResponse(
            "login.html", {"request": request, "msg": msg}
        )


@router.post("/token")
async def login_for_access_token(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):

    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        return False
        # raise HTTPException(
        #     status_code=status.HTTP_401_UNAUTHORIZED,
        #     detail="Could not validate a user",
        # )
    else:
        token = create_access_token(user.username, user.id, timedelta(minutes=20))

        response.set_cookie(key="access_token", value=token, httponly=True)
        return True


@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register", response_class=HTMLResponse)
async def register_user(
    request: Request,
    email: str = Form(...),
    username: str = Form(...),
    firstname: str = Form(...),
    lastname: str = Form(...),
    password: str = Form(...),
    password2: str = Form(...),
    db: Session = Depends(get_db),
):

    validation1 = db.query(Users).filter(Users.username == username).first()

    validation2 = db.query(Users).filter(Users.email == email).first()

    if password != password2 or validation1 is not None or validation2 is not None:
        msg = "Invalid registration request"
        return templates.TemplateResponse(
            "register.html", {"request": request, "msg": msg}
        )

    user_model = Users()
    user_model.username = username
    user_model.email = email
    user_model.first_name = firstname
    user_model.last_name = lastname

    hash_password = get_password_hash(password)
    user_model.hash_password = hash_password
    user_model.is_active = True

    db.add(user_model)
    db.commit()

    msg = "User successfully created"
    return templates.TemplateResponse("login.html", {"request": request, "msg": msg})


@router.get("/logout")
async def logout(request: Request):
    msg = "Logout Successful"
    response = templates.TemplateResponse(
        "login.html", {"request": request, "msg": msg}
    )
    response.delete_cookie(key="access_token")
    return response


@router.get("/change-password", response_class=HTMLResponse)
def change_password(request: Request):
    user = get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth2", status_code=status.HTTP_302_FOUND)
    context = {"request": request, "user": user}
    return templates.TemplateResponse("change-password.html", context)


@router.post("/change-password", response_class=HTMLResponse)
async def change_password_post(
    db: db_dependancy,
    request: Request,
    password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth2", status_code=status.HTTP_302_FOUND)

    user_data = db.query(Users).filter(Users.id == user.get("id")).first()

    print("user data", user_data)
    print(verify_password(password, user_data.hash_password))

    if verify_password(password, user_data.hash_password):
        if new_password != confirm_password:
            msg = "password & confirm password don't match"
            context = {"request": request, "user": user, "msg": msg}
            return templates.TemplateResponse("change-password.html", context)
        else:
            user_data.hash_password = get_password_hash(new_password)
            db.add(user_data)
            db.commit()
            msg = "Password updated"
            context = {"request": request, "user": user, "msg": msg}
            return templates.TemplateResponse("change-password.html", context)
    else:
        msg = "your current password is wrong"
        context = {"request": request, "user": user, "msg": msg}
        return templates.TemplateResponse("change-password.html", context)


def get_password_hash(password):
    print(bcrypt_context.hash(password))
    return bcrypt_context.hash(password)


def verify_password(plain_password, hash_password):
    return bcrypt_context.verify(plain_password, hash_password)


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False
    if not verify_password(password, user.hash_password):
        return False
    return user


async def get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            logout(request)
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=404, detail="Not found")


def create_access_token(
    username: str, user_id: int, expires_delta: Optional[timedelta] = None
):

    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=120)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

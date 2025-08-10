from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select, insert
from app.models.user import User
from app.schemas import CreateUser
from app.backend.db_depends import get_db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings


from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import jwt
from datetime import datetime, timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(prefix="/auth", tags=["auth"])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

session = Annotated[AsyncSession, Depends(get_db)]

# openssl rand -hex 32
SECRET_KEY = settings.SECRET_KEY

ALGORITHM = "HS256"


async def create_access_token(
    username: str,
    user_id: int,
    is_admin: bool,
    is_supplier: bool,
    is_customer: bool,
    expires_delta: timedelta,
):
    encode = {
        "sub": username,
        "id": user_id,
        "is_admin": is_admin,
        "is_supplier": is_supplier,
        "is_customer": is_customer,
    }
    expires = datetime.now() + expires_delta
    encode.update('exp', expires)
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def authenticate_user(db: session, username: str, password: str):
    user = await db.scalar(select(User).where(User.username == username))
    if (
        not user
        or not bcrypt_context.verify(password, user.hashed_password)
        or user.is_active == False
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.post("/token")
async def login(
    db: session,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user or user.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )
    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/read_current_user")
async def read_current_user(user: User = Depends(oauth2_scheme)):
    return user


@router.post("/")
async def create_user(db: session, create_user: CreateUser):
    await db.execute(
        insert(User).values(
            first_name=create_user.first_name,
            last_name=create_user.last_name,
            username=create_user.username,
            email=create_user.email,
            hashed_password=bcrypt_context.hash(create_user.password),
        )
    )
    await db.commit()
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}

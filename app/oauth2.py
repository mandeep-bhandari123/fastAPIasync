from datetime import datetime, timedelta, timezone
from typing import Annotated
from .schemas import Token , TokenData , UserInDB
from .database import get_db
from .model import User

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from dotenv import load_dotenv 
from os import getenv

load_dotenv()

SECRET_KEY= getenv("SECRET_KEY")
ALGORITHM =getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

async def get_user_by_id( id:int,db:AsyncSession):
  result = await db.execute(
    select(User).where(User.id == id)
  )
  user = result.scalar_one_or_none()

  return user

def create_access_token(data:dict , expires_delta: timedelta |None = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now(timezone.utc) + expires_delta
  else:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
  to_encode.update({"exp":expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY , algorithm=ALGORITHM)
  return encoded_jwt

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)]):

  credentials_exception = HTTPException(
  status_code=status.HTTP_401_UNAUTHORIZED,
  detail="Could not validate credentials",
  headers={"WWW-Authenticate": "Bearer"},
    )

  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("sub")

    if user_id is None:
        raise credentials_exception

    token_data = TokenData(id=int(user_id))

  except InvalidTokenError:
      raise credentials_exception

  user = await get_user_by_id(token_data.id, db=db)

  if user is None:
    raise credentials_exception

  return user

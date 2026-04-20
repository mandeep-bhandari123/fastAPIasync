from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel

from dotenv import load_dotenv 
from os import getenv

load_dotenv()

SECRET_KEY= getenv("SECRET_KEY")
ALGORITHM =getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

app = FastAPI()

def create_access_token(data:dict , expires_delta: timedelta |None = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now(timezone.utc) + expires_delta
  else:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
  to_encode.update({"exp":expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY , algorithm=ALGORITHM)
  return encoded_jwt
  
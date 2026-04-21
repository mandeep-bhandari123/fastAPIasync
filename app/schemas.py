from typing import Optional
from pydantic import BaseModel , EmailStr
from datetime import datetime


class User(BaseModel):
   id : int
   email:EmailStr | None = None #Same as optional but modern   | --> is pipe operator which is equivalent to 'or'
   password:str | None = None

class User_Create(BaseModel):
    email:EmailStr
    password:str

class User_Login(BaseModel):
  id:int
  email:EmailStr
  class Config :
      from_attributes=True
class Token(BaseModel):
   access_token:str
   token_type: str 

class TokenData(BaseModel):
  id : int 

class UserInDB(User):
    hashed_password: str

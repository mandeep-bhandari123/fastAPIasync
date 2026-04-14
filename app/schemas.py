from typing import Optional
from pydantic import BaseModel , EmailStr
from datetime import datetime

class User_Create_and_Login(BaseModel):
    email:EmailStr
    password:str

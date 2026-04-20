from fastapi import APIRouter , Depends , status , HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm 
from sqlalchemy.ext.asyncio import AsyncSession
from .. import database , schemas , model , oauth2
from sqlalchemy import select
from ..database import get_db
from ..utils import verify_password


router = APIRouter(tags=["Authentication"])


@router.post("/sign_in", status_code=status.HTTP_202_ACCEPTED , response_model=schemas.User_Login)
async def login(user:schemas.User_Create, db:AsyncSession = Depends(get_db)):
  result = await db.execute(select(model.User).where(model.User.email == user.email))
  existing_user = result.scalar_one_or_none()
  if verify_password(user.password, existing_user.password):
    print(type({existing_user.id : existing_user.email}))
    output = {"id":existing_user.id , "email":existing_user.email}
    return output
  raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Wrong detail")


  

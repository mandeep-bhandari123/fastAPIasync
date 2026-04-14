from .. import model , schemas
from sqlalchemy.ext.asyncio import create_async_engine ,AsyncSession
from fastapi import status , HTTPException , Depends , APIRouter
from sqlalchemy import select

from ..database import get_db

router = APIRouter(
  prefix="/users",
  tags=["Users"]
)
@router.post("/sign_up" ,status_code=status.HTTP_201_CREATED , response_model=schemas.User_Create_and_Login)
async def create_user(user:schemas.User_Create_and_Login , db:AsyncSession = Depends(get_db)):
  result = await db.execute(
    select(model.User).where(model.User.email == user.email)
  )
  existing_user = result.scalar_one_or_none()
  if existing_user:
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail=f"User with {user.email} already exists"
    )
  new_user = model.User(**user.dict())
  db.add(new_user)
  await db.commit()
  await db.refresh(new_user)
  return new_user

@router.post("/sign_in", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.User_Create_and_Login)
async def login(log:schemas.User_Create_and_Login, db:AsyncSession = Depends(get_db)):
  result = await db.execute(
    select(model.User).where(model.User.email == log.email)
  )
  user = result.scalar_one_or_none()
  print(**user.dict())
  if not user or  user.password != model.User.password :
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Invalid email or password")
  return {user.email:"Succesfully logged in"}

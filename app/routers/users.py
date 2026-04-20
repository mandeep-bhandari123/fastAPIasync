from .. import model , schemas
from sqlalchemy.ext.asyncio import create_async_engine ,AsyncSession
from fastapi import status , HTTPException , Depends , APIRouter
from sqlalchemy import select
from ..utils import hash_password , verify_password
from ..database import get_db

router = APIRouter(
  prefix="/users",
  tags=["Users"]
)
@router.post("/sign_up" ,status_code=status.HTTP_201_CREATED , response_model=schemas.User_Create)
async def create_user(user:schemas.User_Create , db:AsyncSession = Depends(get_db)):
  result = await db.execute(
    select(model.User).where(model.User.email == user.email)
  )
  existing_user = result.scalar_one_or_none()
  if existing_user:
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail=f"User with {user.email} already exists"
    )
  hashed_password = hash_password(user.password)
  user.password = hashed_password
  new_user = model.User(**user.dict())
  db.add(new_user)
  await db.commit()
  await db.refresh(new_user)
  return new_user


    

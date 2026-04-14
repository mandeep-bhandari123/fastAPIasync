from fastapi import FastAPI 
from .database import   engine, Base , AsyncSessionLocal
from .routers import users
app = FastAPI()

app.include_router(users.router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def home ():
  return {"Mandeep Bhandari":"Belovolent dictator for life"}



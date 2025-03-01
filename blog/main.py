from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from .database import engine
from .routers import blogs, users

@asynccontextmanager
async def lifespan(app: FastAPI):
  # Create database
  print("Creating database tables")
  SQLModel.metadata.create_all(engine)
  print("Database connected")
  yield
  # Disconnect database
  print("Database disconnected")


app = FastAPI(lifespan=lifespan)

app.include_router(blogs.router)
app.include_router(users.router)




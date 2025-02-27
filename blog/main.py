from contextlib import asynccontextmanager
from fastapi import FastAPI
from . import schemas
from .database import engine, Base
from sqlmodel import SQLModel
from .models import Blog

@asynccontextmanager
async def lifespan(app: FastAPI):
  # Create database
  if len(SQLModel.metadata.tables.keys()) == 0:
    SQLModel.metadata.create_all(engine)
  print("Database connected")
  yield
  # Disconnect database
  print("Database disconnected")


app = FastAPI(lifespan=lifespan)



@app.post('/blog')
def create(blog: schemas.Blog):
  return blog
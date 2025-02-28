from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas
from .database import engine, Base, SessionLocal
from sqlmodel import SQLModel
from .models import Blog, User
from sqlalchemy.orm import Session
from typing import List
from .hashing import Hash


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



def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()



@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
  new_blog = Blog(title=request.title, body=request.body)
  db.add(new_blog)
  db.commit()
  db.refresh(new_blog)
  return new_blog



@app.get('/blog', response_model=List[schemas.ShowBlog], tags=['blogs'])
def all(db: Session = Depends(get_db)):
  blogs = db.query(Blog).all()
  return blogs



@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog, tags=['blogs'])
def show(id, response:Response, db: Session = Depends(get_db)):
  blog = db.query(Blog).filter(Blog.id == id).first()
  if not blog:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not available")
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {'detail': f"Blog with id {id} is not available"}
  return blog




@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id, request:schemas.Blog, db: Session = Depends(get_db)):
  blog = db.query(Blog).filter(Blog.id==id)
  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  
  blog.update({'title': request.title, 'body': request.body})
  db.commit()
  return 'updated'




@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def remove(id, db: Session = Depends(get_db)):
  blog = db.query(Blog).filter(Blog.id==id)
  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  blog.delete(synchronize_session=False)
  db.commit()
  return 'done'



@app.post('/user', response_model=schemas.ShowUser, tags=['users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
  hashed_password = Hash.get_password_hash(request.password)
  new_user = User(name=request.name, email = request.email, password=hashed_password)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user


@app.get('/user/{id}', status_code=200, response_model=schemas.ShowUser, tags=['users'])
def get_user(id, response:Response, db: Session = Depends(get_db)):
  user = db.query(User).filter(User.id == id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} is not available")
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {'detail': f"User with id {id} is not available"}
  return user
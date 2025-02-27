from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas
from .database import engine, Base, SessionLocal
from sqlmodel import SQLModel
from .models import Blog
from sqlalchemy.orm import Session


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



@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
  new_blog = Blog(title=request.title, body=request.body)
  db.add(new_blog)
  db.commit()
  db.refresh(new_blog)
  return new_blog



@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def remove(id, db: Session = Depends(get_db)):
  blog = db.query(Blog).filter(Blog.id==id)
  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  blog.delete(synchronize_session=False)
  db.commit()
  return 'done'



@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request:schemas.Blog, db: Session = Depends(get_db)):
  blog = db.query(Blog).filter(Blog.id==id)
  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  
  blog.update({'title': request.title, 'body': request.body})
  db.commit()
  return 'updated'




@app.get('/blog')
def all(db: Session = Depends(get_db)):
  blogs = db.query(Blog).all()
  return blogs



@app.get('/blog/{id}', status_code=200)
def show(id, response:Response, db: Session = Depends(get_db)):
  blog = db.query(Blog).filter(Blog.id == id).first()
  if not blog:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not available")
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {'detail': f"Blog with id {id} is not available"}
  return blog
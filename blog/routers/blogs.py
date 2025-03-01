from fastapi import APIRouter, Depends, status, HTTPException, Response
from typing import List
from .. import schemas
from ..database import get_db
from ..models import Blog, User
from sqlalchemy.orm import Session


router = APIRouter(
  prefix='/blog',
  tags=['Blogs']
)

@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
  blogs = db.query(Blog).all()
  return blogs


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
  new_blog = Blog(title=request.title, body=request.body, creator_id=1)
  db.add(new_blog)
  db.commit()
  db.refresh(new_blog)
  return new_blog


@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def show(id, response:Response, db: Session = Depends(get_db)):
  blog = db.query(Blog).filter(Blog.id == id).first()
  if not blog:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not available")
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {'detail': f"Blog with id {id} is not available"}
  return blog




@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request:schemas.Blog, db: Session = Depends(get_db)):
  blog = db.query(Blog).filter(Blog.id==id)
  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  
  blog.update({'title': request.title, 'body': request.body})
  db.commit()
  return 'updated'




@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def remove(id, db: Session = Depends(get_db)):
  blog = db.query(Blog).filter(Blog.id==id)
  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  blog.delete(synchronize_session=False)
  db.commit()
  return 'done'
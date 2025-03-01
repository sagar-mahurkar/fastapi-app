from fastapi import Depends, HTTPException, status
from ..database import get_db
from ..models import Blog
from sqlalchemy.orm import Session
from .. import schemas


def get_all(db: Session = Depends(get_db)):
  blogs = db.query(Blog).all()
  return blogs



def create(request: schemas.Blog, db: Session = Depends(get_db)):
  new_blog = Blog(title=request.title, body=request.body, creator_id=1)
  db.add(new_blog)
  db.commit()
  db.refresh(new_blog)
  return new_blog



def show(id: int, db: Session = Depends(get_db)):
  blog = db.query(Blog).filter(Blog.id == id).first()
  if not blog:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not available")
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {'detail': f"Blog with id {id} is not available"}
  return blog




def update(id: int, request:schemas.Blog, db: Session = Depends(get_db)):
  blog = db.query(Blog).filter(Blog.id==id)
  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  
  blog.update({'title': request.title, 'body': request.body})
  db.commit()
  return 'updated'




def remove(id: int, db: Session = Depends(get_db)):
  blog = db.query(Blog).filter(Blog.id==id)
  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  blog.delete(synchronize_session=False)
  db.commit()
  return 'done'
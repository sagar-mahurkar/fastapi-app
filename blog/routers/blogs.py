from fastapi import APIRouter, Depends, status, Response
from typing import List
from .. import schemas
from ..database import get_db
from sqlalchemy.orm import Session
from ..util import blogs

router = APIRouter(
  prefix='/blog',
  tags=['Blogs']
)

@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
  return blogs.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
  return blogs.create(request, db)


@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def show(id: int, db: Session = Depends(get_db)):
  return blogs.show(id, db)




@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request:schemas.Blog, db: Session = Depends(get_db)):
  return blogs.update(id, request, db)




@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def remove(id: int, db: Session = Depends(get_db)):
  return blogs.remove(id, db)
from fastapi import APIRouter, Depends, status, HTTPException, Response
from typing import List
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from ..models import User
from ..hashing import Hash


router = APIRouter(
  prefix='/user',
  tags=['Users']
)




@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
  hashed_password = Hash.get_password_hash(request.password)
  new_user = User(name=request.name, email = request.email, password=hashed_password)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user


@router.get('/{id}', status_code=200, response_model=schemas.ShowUser)
def get_user(id, db: Session = Depends(get_db)):
  user = db.query(User).filter(User.id == id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} is not available")
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {'detail': f"User with id {id} is not available"}
  return user
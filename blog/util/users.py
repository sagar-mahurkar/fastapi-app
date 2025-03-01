
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas
from ..hashing import Hash
from ..models import User
from ..database import get_db


def create(request: schemas.User, db: Session = Depends(get_db)):
  hashed_password = Hash.get_password_hash(request.password)
  new_user = User(name=request.name, email = request.email, password=hashed_password)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user


def get(id: int, db: Session = Depends(get_db)):
  user = db.query(User).filter(User.id == id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} is not available")
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {'detail': f"User with id {id} is not available"}
  return user
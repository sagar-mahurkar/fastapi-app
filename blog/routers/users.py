from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from ..utils import users

router = APIRouter(
  prefix='/user',
  tags=['Users']
)




@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
  return users.create(request, db)


@router.get('/{id}', status_code=200, response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
  return users.get(id, db)
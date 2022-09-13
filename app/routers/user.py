from typing import *
from fastapi import *
from app import models
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import *
from ..utils import hashedPassword
from .. import schemas , models

router = APIRouter(
    tags=['User']
)

@router.post('/create_user' , status_code=status.HTTP_201_CREATED ,  response_model=schemas.ResponseUser)
def create_user(user : schemas.PostUser , db : Session = Depends(get_db)) :
    user.password = hashedPassword(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/user/{id}' , response_model=schemas.ResponseUser)
def get_user(id:int , db:Session = Depends(get_db)):
    fetch_query = db.query(models.User).filter(models.User.id==id)
    required_user = fetch_query.first()
    if required_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'User with id : {id} does not exist')
    return required_user
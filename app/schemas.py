from datetime import datetime
from typing import Optional
from pydantic import BaseModel , EmailStr
from pydantic.types import conint

from app.models import Votes
# does the validation , 
# defines the schema of what the front end sends to us
# this is the schema model or the 'Pydantic' Model 

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True
    
class PostCreate(PostBase):
    pass

class PostUser(BaseModel):
    email : EmailStr
    password : str

class ResponseUser(BaseModel):
    email : EmailStr
    created_at : datetime
    id : int
    class Config:
        orm_mode = True

class PostResponse(PostBase):
    id : int
    created_at : datetime
    user_id : str
    user : ResponseUser
    class Config:
        orm_mode =  True
        
class VotesInfo(BaseModel):
    Post : PostResponse
    votes : int
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[str]=None

class Vote(BaseModel):
    post_id : int
    dir : conint(le=1)

class VoteResponse(BaseModel) :
    post_id : int
    user_id : int





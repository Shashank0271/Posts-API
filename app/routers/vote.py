from app.oauth2 import get_current_user
from .. import schemas , models 
from typing import *
from fastapi import *
from app import models
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import *

router = APIRouter(
    tags=['Votes']
)

@router.post('/vote' , status_code=status.HTTP_201_CREATED)
def vote(vote : schemas.Vote , db : Session = Depends(get_db) , current_user : models.User = Depends(get_current_user)):
    
    if db.query(models.Votes).filter(models.Votes.post_id == vote.post_id).first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id {vote.post_id} does not exist")
    
    vote_query = db.query(models.Votes).filter(models.Votes.user_id == current_user.id and models.Votes.post_id == vote.post_id)
    found_vote = vote_query.first() 
    if vote.dir == 1:
        if found_vote :
            raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail='you cannot like a vote twice')
        add_vote = models.Votes(user_id = current_user.id , post_id=vote.post_id)
        db.add(add_vote)
        db.commit()
        return {"message " : "voted !" }
    else:
        if found_vote == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="post to be deleted doesn't exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message ": "vote removed !"}

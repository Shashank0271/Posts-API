
from app.oauth2 import get_current_user
from .. import schemas , models 
from typing import *
from fastapi import *
from app import models
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import *

router = APIRouter(
    tags=['Posts']
)

@router.get('/joins' , response_model = List[schemas.VotesInfo])
def joinf(db : Session = Depends(get_db)):
    result = db.query(models.Post , func.count(models.Votes.post_id).label("votes")).join(models.Votes , models.Votes.post_id == models.Post.id , isouter=True).group_by(models.Post.id).all()
    return result

@router.get("/myposts" , response_model = List[schemas.PostResponse])
def get_current_users_posts(db : Session = Depends(get_db) , current_user : models.User = Depends(get_current_user)):
    my_posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    return my_posts

@router.get("/allposts" , response_model = List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # return posts  
    posts = db.query(models.Post).all()
    return posts

@router.post('/create_post' , status_code=status.HTTP_201_CREATED , response_model=schemas.PostResponse)
def create_post(payload: schemas.PostCreate , db: Session = Depends(get_db) , user : models.User = Depends(get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title , content , published) VALUES (%s ,%s ,%s) RETURNING * """,(payload.title , payload.content , payload.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # return {'data' : new_post}
    print(payload.dict())
    new_post = models.Post(user_id=user.id,**payload.dict())
    db.add(new_post)
    db.commit()
    return new_post  

@router.get('/get_single_post/{id}' ,  response_model=schemas.VotesInfo)
def get_single_post(id : int , db: Session = Depends(get_db) , user : models.User = Depends(get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """ , (str(id)))
    # post = cursor.fetchone()
    # print(post) 
    post = db.query(models.Post , func.count(models.Votes.post_id).label("votes")).filter(models.Post.id == id).join(models.Votes , models.Votes.post_id == models.Post.id , isouter=True).group_by(models.Post.id).first()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , 
            detail=f"post with rating {id} not found")
    return post

@router.delete('/delete/{id}' , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int , db: Session = Depends(get_db) , user : models.User = Depends(get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s returning * """ , (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post_query = db.query(models.Post).filter(models.Post.id==id)
    req_post = deleted_post_query.first()
    
    if req_post == None:
        raise HTTPException(detail = f'post with id {id} does not exist' , status_code=status.HTTP_404_NOT_FOUND)
    
    if req_post.user_id != user.id:
        raise HTTPException(detail = "Not authorized to perform required action" ,status_code=status.HTTP_401_UNAUTHORIZED) 
    
    deleted_post_query.delete(synchronize_session=False)
    db.commit()

@router.put('/update_post/{id}' ,  response_model=schemas.PostResponse)
def update_post(id:int , post:schemas.PostBase , db: Session = Depends(get_db) , user : models.User = Depends(get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING * """ , (post.title , post.content , post.published , str(id)))
    # updated_post = cursor.fetchone() 
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    req_post = post_query.first()
    if req_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'post with id {id} does not exist')
    if req_post.user_id != user.id:
        raise HTTPException(detail = "Not authorized to perform required action" ,status_code=status.HTTP_401_UNAUTHORIZED) 
    
    post_query.update(post.dict() , synchronize_session=False)
    db.commit()
    return {"updated post " : post_query.first()} 
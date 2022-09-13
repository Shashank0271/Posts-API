# to create venv : py -3 -m <venvname> venv
# to enable venv on terminal : venv\Scripts\activate
# to start server : uvicorn app.main:app --reload 
from time import sleep
# from pydantic import BaseModel
from typing import *
from fastapi import *
# import psycopg2
# from psycopg2.extras import RealDictCursor
from . import models
from app.database import get_db
from app.database import engine
from sqlalchemy.orm import Session
from sqlalchemy import *
from .routers import posts , user , auth , vote
from fastapi.middleware.cors import CORSMiddleware
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

get_db()

# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost' , database = 'fastapi' , user='shashank' , password='shashank' , cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successfull!")
#         break
#     except Exception as error:
#         print('connecting to db failed')
#         print(error)
#         sleep(2)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#-------------------------------------------------------------------------------------

@app.get('/testpoint1')
def func(db : Session = Depends(get_db)):
    #1. to get row having a particular name :
    query = db.query(models.Post).filter(models.Post.id.__eq__(1))
    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'not found')

@app.get('/testpoint2')
def func2(db : Session = Depends(get_db)):
    #2. 'LIKE' clause
    query = db.query(models.Post).where(models.Post.title.like('%title%'))
    return {"data " : query.all()}

@app.get('/testpoint3')
def func3(db : Session = Depends(get_db)):
    #3. 'AND' clause
    query = db.query(models.Post).where(and_(models.Post.title.like('%title') , models.Post.content.like('%content')))
    return query.all()

@app.get('/testpoint4')
def func4(db : Session = Depends(get_db)):
    #4. ORDER BY clause
    query = db.query(models.Post).order_by(models.Post.content)
    return {'data':query.all()}


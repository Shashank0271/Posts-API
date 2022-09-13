#every model represents a table in our database
from tkinter import CASCADE
from .database import Base 
from sqlalchemy import Integer , String , Boolean , Column , ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer , primary_key=True, nullable=False)
    title = Column(String , nullable=False)
    content = Column(String , nullable=False)
    published = Column(Boolean , server_default='TRUE' , nullable=False)
    created_at = Column(TIMESTAMP(timezone=True) ,server_default=text('now()') , nullable=False )
    user_id = Column(Integer , ForeignKey("users.id",ondelete="CASCADE") , nullable=False)
    user = relationship("User")
    
    def __repr__(self):
       return "<Post(title='%s', content='%s', published='%s')>" % (self.title, self.content, self.published)    


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer , primary_key=True, nullable=False)
    email = Column(String , nullable=False , unique=True)
    password = Column(String , nullable=False)
    created_at = Column(TIMESTAMP(timezone=True) ,server_default=text('now()') , nullable=False )
    def __repr__(self):
       return "<User(email='%s', created_at='%s'')>" % (self.email, self.created_at)    

class Votes(Base):
    __tablename__ = 'votes'
    user_id = Column(Integer ,ForeignKey("users.id" , ondelete="CASCADE"), primary_key=True , nullable=False)
    post_id = Column(Integer ,ForeignKey("posts.id" , ondelete="CASCADE"), primary_key=True , nullable=False)
    
    def __repr__(self) -> str:
        return f"<Votes user_id :{self.user_id}, post_id :{self.post_id}>"
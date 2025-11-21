from pydantic import BaseModel

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "User"
    
    user_id = Column(String(100), primary_key=True, index=True)
    password = Column(String(100))
    nickname = Column(String(100))
    img_id = Column(String(100))

# class User(BaseModel) : 
#     user_id : str
#     password : str
#     nickname : str
#     img_id : str

class Post(BaseModel) : 
    post_id : str
    user_id : str
    title : str
    content : str
    img_id : str
    view_cnt : int
    create_time : str

class Comment(BaseModel) : 
    comment_id : str
    post_id : str
    user_id : str
    content : str
    create_time : str

class Like(BaseModel) : 
    user_id : str
    post_id : str

class File(BaseModel) : 
    img_id : str
    img_url : str
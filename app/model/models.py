from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

# --- File 테이블 ---
class File(Base):
    __tablename__ = "File"
    img_id = Column(String(50), primary_key=True) # 기본 키만 유지
    img_url = Column(String(255), nullable=False)

# --- User 테이블 ---
class User(Base):
    __tablename__ = "User"
    user_id = Column(String(50), primary_key=True)
    password = Column(String(255), nullable=False)
    nickname = Column(String(100), nullable=False) # UNIQUE 제약조건 제거
    img_id = Column(String(50)) # 외래키 정보 제거

# --- Post 테이블 ---
class Post(Base):
    __tablename__ = "Post"
    post_id = Column(String(50), primary_key=True)
    user_id = Column(String(50), nullable=False) # 외래키 정보 제거
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    img_id = Column(String(50)) # 외래키 정보 제거
    view_cnt = Column(Integer, nullable=False, default=0)
    create_time = Column(DateTime, nullable=False, default=datetime.utcnow) 

# --- Comment 테이블 ---
class Comment(Base):
    __tablename__ = "Comment"
    comment_id = Column(String(50), primary_key=True)
    post_id = Column(String(50), nullable=False) # 외래키 정보 제거
    user_id = Column(String(50), nullable=False) # 외래키 정보 제거
    content = Column(Text, nullable=False)
    create_time = Column(DateTime, nullable=False, default=datetime.utcnow)

# --- PostLike 테이블 ---
class PostLike(Base):
    __tablename__ = "PostLike"
    # 복합키 제약조건 및 외래키 정보 모두 제거
    user_id = Column(String(50), primary_key=True) # PK를 user_id에 임시 설정 (ORM 매핑을 위해 필요)
    post_id = Column(String(50), nullable=False)
from .database import Base
from sqlalchemy import Column , Integer, Boolean,String,TIMESTAMP, text,ForeignKey
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__="posts"
    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,nullable=False,default=True)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner=relationship("User")

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,nullable=False,autoincrement=True,unique=True)
    email=Column(String,primary_key=True,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

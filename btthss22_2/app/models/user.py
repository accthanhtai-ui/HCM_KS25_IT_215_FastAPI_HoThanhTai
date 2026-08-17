from app.db.database import Base
from sqlalchemy import Column,Integer,String

class User(Base):
    __table__ ="users"
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    User = Column(String(255),nullable=False,unique=True)
    hashed_password = Column(String(100),nullable=False)
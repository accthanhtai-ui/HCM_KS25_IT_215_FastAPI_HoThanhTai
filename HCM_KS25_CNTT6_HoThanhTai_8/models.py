from sqlalchemy import Column,String,Integer,Float
from database import Base

class TeamModel(Base):
    __tablename__ = "teams"
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    customer_name = Column(String(100),nullable=False)
    product_code = Column(String(100),nullable=False)
    total_amount = Column(Float)
    status = Column(String(50),nullable=False,index=True)
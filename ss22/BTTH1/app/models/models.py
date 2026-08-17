from app.db.database import Base
from sqlalchemy import Integer, String, Column

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(100), nullable=False)
from sqlalchemy import Column, Integer, String, Float
from ..database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    major = Column(String(255), nullable=True)
    gpa = Column(Float, nullable=True)

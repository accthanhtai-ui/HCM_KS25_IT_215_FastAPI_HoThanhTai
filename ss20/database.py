from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "mysql+pymysql://root:@localhost:3306/student_management_db"

engine = create_engine(DATABASE_URL)

LocalSession = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = LocalSession()

    try:
        yield db
    finally:
        db.close()
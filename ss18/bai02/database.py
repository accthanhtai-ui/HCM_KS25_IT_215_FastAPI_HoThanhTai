from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Thay mật khẩu MySQL của bạn vào đây
DATABASE_URL = "mysql+pymysql://root:123456@localhost/workshop_db"

engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
from sqlalchemy.orm import Session
from schemas import UserRequestDTo
from models import UserModel
from sqlalchemy.exc import SQLAlchemyError

# them du lieu
def create_user(db: Session, user: UserRequestDTo):
    try:
        new_user = UserModel(
            name = user.name,
            email = user.email
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except SQLAlchemyError as s:
        db.rollback()
        raise s 

# lay du lieu
def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

# cap nhat du lieu
def update_user(db: Session, user_id: int, user: UserRequestDTo):
    try:
        db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            return None
        db_user.name = user.name
        db_user.email = user.email
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as s:
        db.rollback()
        raise s
    
# xoa du lieu
def delete_user(db: Session, user_id: int):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user

# tim kiem du lieu
def search_users(db: Session, name: str = None, email: str = None):
    query = db.query(UserModel)
    if name:
        query = query.filter(UserModel.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(UserModel.email.ilike(f"%{email}%"))
    return query.all()
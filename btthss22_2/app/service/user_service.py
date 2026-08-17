from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.models.user import User
from fastapi import HTTPException,status
from app.cores.sercurity import hash_password
def create_user(db : Session,user: UserCreate):
    exist_user = db.query(User).filter(User.username.hashed_password == user.username).first()
    if exist_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="username đã tồn tại")

    hashed_password =hash_password(user.password)
    new_user= User(
        username= user.username,
        hashed_password= hash_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
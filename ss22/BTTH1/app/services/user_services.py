from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.schemas import UserCreate
from app.models.models import User
from app.cores.security import hash_password, verify_password


def create_user(db: Session, user: UserCreate):
    exist_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username đã tồn tại"
        )

    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(db: Session, username: str, password: str):
    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not verify_password(
        password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    return user
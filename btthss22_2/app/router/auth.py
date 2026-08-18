from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse
import app.service.user_service as user_service


router_auth = APIRouter(
    prefix="/api",
    tags=["authentication"]
)


@router_auth.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    data = user_service.create_user(db, user)
    return data
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.schemas import (
    UserCreate,
    UserResponse,
    LoginRequest,
    TokenResponse,
    ProfileResponse
)
from app.services.user_services import create_user, login_user
from app.cores.security import (
    create_access_token,
    verify_access_token
)


auth_all = APIRouter(
    prefix="/api",
    tags=["Authentication"]
)

security = HTTPBearer()


@auth_all.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user(db, user)


@auth_all.post(
    "/login",
    response_model=TokenResponse
)
def login(
    user: LoginRequest,
    db: Session = Depends(get_db)
):
    db_user = login_user(
        db,
        user.username,
        user.password
    )

    access_token = create_access_token(
        db_user.username
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@auth_all.get(
    "/profile",
    response_model=ProfileResponse
)
def profile(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    username = verify_access_token(token)

    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    return {
        "message": f"Welcome, {username}!"
    }
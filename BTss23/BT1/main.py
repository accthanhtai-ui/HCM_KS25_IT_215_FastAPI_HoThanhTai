from datetime import datetime, timedelta, timezone

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt


app = FastAPI()


# Cấu hình JWT
SECRET_KEY = "training-secret-key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Danh sách người dùng giả lập
USERS = {
    "alice": {
        "username": "alice",
        "full_name": "Alice Nguyen",
        "role": "user",
        "is_active": True,
    },
    "bob": {
        "username": "bob",
        "full_name": "Bob Tran",
        "role": "user",
        "is_active": False,
    },
}


# API tạo token để test
@app.get("/issue-token/{username}")
def issue_token(username: str, expired: bool = False):

    if username not in USERS:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=-5 if expired else 30
    )

    token = jwt.encode(
        {
            "sub": username,
            "exp": expires_at,
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


# Dependency kiểm tra người dùng hiện tại
def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    try:
        # Kiểm tra chữ ký và thời hạn của token
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Lấy username từ trường sub
        username = payload.get("sub")

        # Token không có sub
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    except JWTError:
        # Token sai chữ ký hoặc đã hết hạn
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    # Kiểm tra tài khoản có tồn tại không
    user = USERS.get(username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    # Kiểm tra tài khoản có đang hoạt động không
    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive"
        )

    return user


# API lấy thông tin người dùng hiện tại
@app.get("/users/me")
def read_current_user(
    current_user: dict = Depends(get_current_user)
):
    return current_user
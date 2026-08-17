import os
import bcrypt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from jose import JWTError, jwt


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


if not SECRET_KEY:
    raise ValueError("SECRET_KEY chưa được cấu hình trong file .env")


def hash_password(password: str, cost_factor: int = 12):
    # chuyển đổi pass từ string sang byte
    password_byte = password.encode("utf-8")

    # sinh ra 1 đoạn salt ngẫu nhiên
    salt = bcrypt.gensalt(rounds=cost_factor)

    # tiến hành băm mật khẩu
    hashed_password = bcrypt.hashpw(password_byte, salt)

    # trả về mật khẩu đã được chuyển về dạng string
    return hashed_password.decode("utf8")


def verify_password(password: str, hashed_password: str):
    password_byte = password.encode("utf-8")
    hashed_password_byte = hashed_password.encode("utf-8")

    return bcrypt.checkpw(
        password_byte,
        hashed_password_byte
    )


def create_access_token(username: str):
    now = datetime.now(timezone.utc)

    expire = now + timedelta(minutes=30)

    payload = {
        "sub": username,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp())
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if not username:
            return None

        return username

    except JWTError:
        return None
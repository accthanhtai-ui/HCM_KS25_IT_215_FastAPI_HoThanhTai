import os

from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import JWTError, jwt


load_dotenv()

MEDCARE_SECRET_KEY = os.getenv("MEDCARE_SECRET_KEY")

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 20


if not MEDCARE_SECRET_KEY:
    raise ValueError(
        "MEDCARE_SECRET_KEY chưa được cấu hình trong file .env"
    )


def create_access_token(username: str, role: str):
    now = datetime.now(timezone.utc)

    expire = now + timedelta(minutes=20)

    payload = {
        "sub": username,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp())
    }

    token = jwt.encode(
        payload,
        MEDCARE_SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            MEDCARE_SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")
        role = payload.get("role")

        if not username or not role:
            return None

        return {
            "username": username,
            "role": role
        }

    except JWTError:
        return None
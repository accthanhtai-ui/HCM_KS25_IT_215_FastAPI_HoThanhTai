from fastapi import HTTPException, status

from app.cores.password import hash_password, verify_password


# lưu tài khoản trong RAM
medical_users = {}


def register_medical_user(
    username: str,
    password: str,
    role: str
):
    if username in medical_users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username đã tồn tại"
        )

    hashed_password = hash_password(password)

    medical_users[username] = {
        "username": username,
        "hashed_password": hashed_password,
        "role": role
    }

    return {
        "username": username,
        "role": role
    }


def login_medical_user(
    username: str,
    password: str
):
    user = medical_users.get(username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Thông tin đăng nhập không chính xác"
        )

    check_password = verify_password(
        password,
        user["hashed_password"]
    )

    if not check_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Thông tin đăng nhập không chính xác"
        )

    return user
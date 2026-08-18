import bcrypt


def hash_password(password: str, cost_factor: int = 12):
    # chuyển password từ string sang byte
    password_byte = password.encode("utf-8")

    # sinh salt ngẫu nhiên
    salt = bcrypt.gensalt(rounds=cost_factor)

    # băm mật khẩu
    hashed_password = bcrypt.hashpw(
        password_byte,
        salt
    )

    # chuyển về string
    return hashed_password.decode("utf-8")


def verify_password(password: str, hashed_password: str):
    # chuyển password nhập vào thành byte
    password_byte = password.encode("utf-8")

    # chuyển hash đã lưu thành byte
    hashed_password_byte = hashed_password.encode("utf-8")

    # kiểm tra password
    return bcrypt.checkpw(
        password_byte,
        hashed_password_byte
    )
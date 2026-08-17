import bcrypt

def hash_password(password:str,cost_factor:int = 12):
    # chuyển đổi string sang byte
    password_byte = password.encode("utf-8")
    #sinh ra một đoạn salt ngẫu nhiên
    salt = bcrypt.gensalt(rounds=cost_factor)
    #tiến hành băm mật khẩu
    hashed_password = bcrypt.hashpw(password_byte,salt)
    return hashed_password.decode("utf-8")
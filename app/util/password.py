#
import bcrypt


def hash_password(password: str):  # 加密后的密码
    """加密pwd"""
    return bcrypt.hashpw(  # hashpw 开始加密-返回的是二进制
        # 加密
        password.encode("utf-8"),
        # 随机生成一串字符串gensalt
        bcrypt.gensalt(),
    ).decode(
        # decode 把二进制解析成普通的字符串
        "utf-8"
    )


# print("salt", hash_password("123"))


def verify_password(password: str, hashed_password: str) -> bool:
    """前后端密码比较"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

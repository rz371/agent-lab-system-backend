from fastapi import Depends
from sqlalchemy.orm import Session
from app.common.exceptions import BusinessException
from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest
from app.schemas.user import UserResponse
from app.util import password
from app.util.jwt import create_access_token
from app.util.password import hash_password, verify_password


def login(data: LoginRequest, db: Session):
    print("登录", data)
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not verify_password(data.password, user.password):
        # return {"code": 400, "message": "账号或密码错误"}
        # return Response.error(message="账号或密码错误")
        raise BusinessException(message="账号或密码错误")

    if user.status != 1:
        # return {"code": 403, "message": "账号已被禁用"}
        # return Response.error(message="账号已被禁用")
        raise BusinessException(code=403, message="账号已被禁用")
    token = create_access_token(user.id)
    return LoginResponse(token=token, user=UserResponse.model_validate(user))


def register(data: RegisterRequest, db: Session):
    # 先看看有没有账号吧
    user = db.query(User).filter(data.username == User.username).first()
    if not user:
        new_col = User(
            username=data.username,
            password=hash_password(data.password),
            name=data.name or data.username,
            role="student",
            status=1,
        )
        db.add(new_col)
        db.commit()
        db.refresh()
        return "已成功注册"
    else:
        raise BusinessException(message="已有账号，请去登录")

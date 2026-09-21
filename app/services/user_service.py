from fastapi import Depends

from app.common.exceptions import BusinessException
from app.dependencies.auth import get_current_user
from app.schemas.user import UserResponse


def get_userinfo(user: str = Depends(get_current_user)):
    """获取用户信息"""
    if not user:
        raise BusinessException(message="账号或密码错误")

    if user.status != 1:
        raise BusinessException(code=403, message="用户被禁止访问")

    return UserResponse.model_validate(user)

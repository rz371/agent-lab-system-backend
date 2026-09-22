from fastapi import Depends

from app.common.exceptions import BusinessException
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import UpdatePasswordRequest, UserResponse, UserUpdateRequest
from sqlalchemy.orm import Session

from app.util.password import hash_password, verify_password


def get_userinfo(user: User):
    """获取用户信息"""
    return UserResponse.model_validate(user)


def update_user_info(
    db: Session,
    user: User,
    data: UserUpdateRequest,
):
    """更新个人信息"""
    # 把 data里面的信息更新到user里面
    # 1、把数据变为dict
    user_dict = data.model_dump(exclude_none=True)
    for key, value in user_dict.items():
        setattr(user, key, value)

    db.commit()  # 提交
    db.refresh(user)  # 刷新
    return UserResponse.model_validate(user)


def update_pwd(db: Session, user: User, data: UpdatePasswordRequest):
    """修改密码逻辑
    新密码不可以与原密码一致，
    """
    if not data.old_pwd:
        raise BusinessException(message="原密码不可为空")
    if verify_password(data.new_pwd, user.password):
        raise BusinessException(message="新密码不可以与原密码一致")

    user.password = hash_password(data.new_pwd)
    db.commit()
    return "密码修改成功"

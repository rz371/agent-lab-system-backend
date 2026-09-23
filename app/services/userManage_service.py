import keyword
from operator import or_

from sqlalchemy import desc

from app.common.exceptions import BusinessException
from app.common.response import pageResponse
from app.models.user import User
from app.schemas.user import (
    UserCreateRequest,
    UserDeleteRequest,
    UserInfoPageRequest,
    UserResponse,
    UserUpdateRequest,
)
from sqlalchemy.orm import Session

from app.util import password


def get_user_manager_all(data: UserInfoPageRequest, db: Session):
    """获取用户管理的所有信息接口逻辑"""
    # 判断有没有keyword
    query = db.query(User)
    if data.keyword:
        query = query.filter(
            # 多关键字查询用or_
            # SQL 用OR
            or_(
                User.username.like(f"%{data.keyword}%"),
                User.name.like(f"%{data.keyword}%"),
            )
        )

    total = query.count()

    # 分页，用offset 和limit 进行控制
    items = (
        query.order_by(User.id.desc())
        .offset((data.page - 1) * data.size)
        .limit(data.size)
        .all()
    )
    # items 结果是一个orm对象，需要变为JSON
    # 返回 -- 分页返回应该格式一样
    return pageResponse(
        total=total, list=[UserResponse.model_validate(item) for item in items]
    )


def create_user_se(data: UserCreateRequest, db: Session):
    """新增用户"""
    exist = db.query(User).filter(User.username == data.username).first()
    if exist:
        raise BusinessException(message="用户已存在")

    user = User(
        username=data.username,
        password=password.hash_password(data.password),
        role=data.role,
        status=data.status,
        name=data.name or data.username,
        avatar=data.avatar,
        email=data.email,
        phone=data.phone,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)


def update_user_se(data: UserUpdateRequest, db: Session):
    """
    用户编辑
    更新通过主键去更新
    """
    print(data)
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise BusinessException(message="用户不存在")
    items = data.model_dump(
        # 在管理员进行用户编辑的话，可以包含"role", "status"
        exclude_none=True,
        exclude={"role", "status"},
    )  # 只取真正传值的
    for key, value in items.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)


def delete_user_se(data: UserDeleteRequest, current_user, db: Session):
    """用户删除"""
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise BusinessException(message="用户不存在")

    if user.id == current_user.id:
        raise BusinessException(message="不可删除当前登录用户")

    db.delete(user)
    db.commit()
    return "已成功删除"

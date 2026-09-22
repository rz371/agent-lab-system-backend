import keyword
from operator import or_

from sqlalchemy import desc

from app.common.response import pageResponse
from app.models.user import User
from app.schemas.user import UserInfoPageRequest, UserResponse
from sqlalchemy.orm import Session


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

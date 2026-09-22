from fastapi import Depends, APIRouter
from app.common.response import Response
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserUpdateRequest
from app.services import user_service
from sqlalchemy.orm import Session

router = APIRouter(prefix="/user", tags=["用户"])


@router.get("/info")
def get_user_info(user: str = Depends(get_current_user)):
    """获取当前登录用户信息"""
    res = user_service.get_userinfo(user)
    return Response.success(data=res)


@router.put("/update")
def update_user_info(
    data: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    更新个人信息,
    必须是已经登录的用户才可以进行更新个人信息
    校验token，就是Depends(get_current_user)
    """
    res = user_service.update_user_info(db, current_user, data)
    return Response.success(data=res)

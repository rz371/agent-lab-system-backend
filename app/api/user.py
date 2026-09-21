from fastapi import Depends, APIRouter
from app.common.response import Response
from app.dependencies.auth import get_current_user
from app.services import user_service

router = APIRouter(prefix="/user", tags=["用户"])


@router.get("/info")
def get_current_user(user: str = Depends(get_current_user)):
    """获取当前用户信息"""
    res = user_service.get_userinfo(user)
    return Response.success(data=res)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.common.response import Response
from app.database import get_db
from app.dependencies.auth import get_current_admin, get_current_user
from app.models.user import User
from app.schemas.user import (
    UserCreateRequest,
    UserDeleteRequest,
    UserInfoPageRequest,
    UserUpdateRequest,
)
from app.services import userManage_service

router = APIRouter(prefix="/user/manager", tags=["用户管理"])


@router.get("/all")
def get_user_info_all(
    # GET 请求不能用 data: UserInfoPageRequest 直接声明，
    # 因为 FastAPI 看到 Pydantic 模型默认从 body 读，而 GET 没有 body，会报 422。
    #
    # 正确写法：data: UserInfoPageRequest = Depends()
    # Depends() 不传参数时，会把模型的每个字段当作 query 参数解析，
    # 从 URL 里读 ?page=1&size=10&keyword=xxx。
    #
    # 注意：Depends(函数) 和 Depends() 不一样。
    # 前者是执行函数拿返回值，后者才是"把模型当 query 解析"。
    data: UserInfoPageRequest = Depends(),
    # fastapi在解析函数签名的时候，会执行所有依赖
    # 先解析所有依赖 → 全部通过后才执行路由函数
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """获取用户管理的所有信息"""
    res = userManage_service.get_user_manager_all(data, db)
    return Response.success(data=res)


@router.post("/create")
def create_user(
    data: UserCreateRequest,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """新增用户"""
    res = userManage_service.create_user_se(data, db)
    return Response.success(data=res)


@router.post("/update")
def update_user(
    data: UserUpdateRequest,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """编辑用户"""
    res = userManage_service.update_user_se(data, db)
    return Response.success(message="编辑成功", data=res)


@router.post("/delete")
def delete_user(
    data: UserDeleteRequest,
    is_admin: User = Depends(get_current_admin),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """删除用户"""
    res = userManage_service.delete_user_se(data, current_user, db)
    return Response.success(data=res)

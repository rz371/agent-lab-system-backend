from fastapi import Depends, APIRouter, HTTPException
from app.common.exceptions import BusinessException
from app.dependencies.auth import get_current_user
from app.schemas.user import UserResponse

router = APIRouter(prefix="/user", tags=["用户"])


@router.get("/info")
def get_current_user(user: str = Depends(get_current_user)):
    """获取当前用户信息"""

    if not user:
        raise BusinessException(message="账号或密码错误")
        # return {"code": 400, "message": "账号或密码错误"}

    if user.status != 1:
        return {"code": 403, "message": "用户被禁止访问"}

    return {
        "code": 200,
        "message": "操作成功",
        "data": UserResponse.model_validate(user),
    }

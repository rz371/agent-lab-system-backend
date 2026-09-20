from fastapi import APIRouter, Depends
from app.common.exceptions import BusinessException
from app.common.response import Response
from app.schemas.auth import LoginRequest, LoginResponse
from app.schemas.user import UserResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.util.jwt import create_access_token
from app.util.password import hash_password, verify_password

# 所有关于权限验证的都可以写到这个py里面

router = APIRouter(prefix="/auth", tags=["权限验证"])


@router.post("/login")
# Session=Depends(get_db) 依赖注入,自动拿数据库会话db
def login(data: LoginRequest, db: Session = Depends(get_db)):
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

    # user 是数据库查出来的ORM对象
    # return {
    #     "code": 200,
    #     "message": "操作成功",
    #     # model_validate() pydantic方法,把外面的数据,转成UserResponse实例
    #     # 等价于:把数据库查出来的数据(ORM对象),交给UserResponse处理,生成一个schema对象,
    #     # 放到返回的JSON里面 , 做这个也是因为UserResponse里面写了model_config = ConfigDict(from_attributes=True)
    #     # 不然model_validate()也报错!!
    #     "data": {"token": token, "user": UserResponse.model_validate(user)},
    # }

    # return Response.success(
    #     data={"token": token, "user": UserResponse.model_validate(user)}
    # )

    return Response.success(
        message="登录成功",
        data=LoginResponse(token=token, user=UserResponse.model_validate(user)),
    )

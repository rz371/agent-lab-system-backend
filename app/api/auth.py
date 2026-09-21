from fastapi import APIRouter, Depends
from app.common.response import Response
from app.schemas.auth import LoginRequest, RegisterRequest
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import auth

# 所有关于权限验证的都可以写到这个py里面

router = APIRouter(prefix="/auth", tags=["权限验证"])


@router.post("/login")
# Session=Depends(get_db) 依赖注入,自动拿数据库会话db
def login(data: LoginRequest, db: Session = Depends(get_db)):
    result = auth.login(data, db)
    # region
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
    # endregion
    return Response.success(
        message="登录成功",
        data=result,
    )


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):

    result = auth.register(data, db)
    return Response.success(message="注册成功", data=result)

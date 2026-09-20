from fastapi import APIRouter, Depends
from app.schemas.auth import LoginRequest
from app.schemas.user import UserResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
# 所有关于权限验证的都可以写到这个py里面

router = APIRouter(prefix='/auth',tags=['权限验证'])

@router.post('/login')
# Session=Depends(get_db) 依赖注入,自动拿数据库会话db
async def login(data:LoginRequest,db:Session=Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    print('有么有',user)
    # or user.password != data.password
    if not user :
        return {'code':400,'message':'账号或密码错误'}

    # user 是数据库查出来的ORM对象
    return {
        "code": 200,
        "message": "操作成功",
        # model_validate() pydantic方法,把外面的数据,转成UserResponse实例
        # 等价于:把数据库查出来的数据(ORM对象),交给UserResponse处理,生成一个schema对象,
        # 放到返回的JSON里面 , 做这个也是因为UserResponse里面写了model_config = ConfigDict(from_attributes=True)
        # 不然model_validate()也报错!!
        "data": UserResponse.model_validate(user),
    }

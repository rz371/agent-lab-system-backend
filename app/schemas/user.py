from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    id: int
    # create_time:datetime
    # update_time:datetime
    username: str
    name: str
    role: str
    status: int
    # 得给一个默认值None，不然BaseModel校验的话就校验必须有值，
    # 会报错
    email: str | None = None
    phone: str | None = None
    avatar: str | None = None

    # 现在从数据库拿出来的是ORM对象,是一个python对象,
    # 而pydantic 只会读dict,这样就直接报错
    # from_attributes=True 开启后,pydantic会自动读ORM对象
    # 注意:如果后端给前端返回数据了,而且这个数据是从数据库ORM来的,就要加这行
    model_config = ConfigDict(from_attributes=True)


class UserUpdateRequest(BaseModel):
    name: str | None = None
    avatar: str | None = None
    phone: str | None = None
    email: str | None = None


class UpdatePasswordRequest(BaseModel):
    old_pwd: str
    new_pwd: str


class UserInfoPageRequest(BaseModel):
    """
    用户信息页面的请求
    页码，页数，根据什么字段进行查询
    """

    size: int
    page: int
    keyword: str | None = None


class UserCreateRequest(BaseModel):
    """用户新增"""

    username: str
    password: str = "123"
    role: str = "student"
    status: int = 1
    name: str | None = None
    avatar: str | None = None
    email: str | None = None
    phone: str | None = None


class UserUpdateRequest(BaseModel):
    """用户编辑"""

    user_id: int
    password: str | None = None
    role: str | None = None
    status: int | None = None
    name: str | None = None
    avatar: str | None = None
    email: str | None = None
    phone: str | None = None


class UserDeleteRequest(BaseModel):
    user_id: int

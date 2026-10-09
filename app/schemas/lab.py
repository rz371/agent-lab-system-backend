from pydantic import BaseModel, ConfigDict


class LabResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    img: str | None = None
    location: str | None = None
    capacity: int
    open_time: str | None = None
    close_time: str | None = None
    status: int

    # 这个是后端给前端返回的，所以必须要加下面这一行
    # 目的：让pydantic自动读取orm对象
    # 原本的pydantic只能读dict
    # 而从数据库拿来的orm对象是一个python对象，pydantic无法读取
    model_config = ConfigDict(from_attributes=True)


class LabCreateRequest(BaseModel):
    """新增实验室"""

    name: str
    description: str | None = None
    img: str | None = None
    location: str | None = None
    capacity: int = 0
    open_time: str | None = None
    close_time: str | None = None
    status: int = 1


class LabUpdateRequest(BaseModel):
    """编辑实验室"""

    lab_id: int
    name: str | None = None
    description: str | None = None
    img: str | None = None
    location: str | None = None
    capacity: int | None = None
    open_time: str | None = None
    close_time: str | None = None
    status: int | None = None


class LabDeleteRequest(BaseModel):
    """删除实验室"""

    lab_id: int


class LabPageRequest(BaseModel):
    """实验室分页请求"""

    size: int
    page: int
    keyword: str | None = None

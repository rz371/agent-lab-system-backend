from pydantic import BaseModel, ConfigDict

from app.models.equipment import EquipStatus


class EquipmentResponse(BaseModel):
    """后端给前端响应的"""

    id: int
    lab_id: int
    lab_name: str | None = None
    name: str
    description: str | None = None
    img: str | None = None
    spec: str | None = None
    quantity: int
    status: int

    model_config = ConfigDict(from_attributes=True)


class EquipmentCreateRequest(BaseModel):
    """增"""

    lab_id: int
    name: str
    description: str | None = None
    img: str | None = None
    spec: str | None = None
    quantity: int = 1
    status: int = EquipStatus.ENABLED.value


class EquipmentUpdateRequest(BaseModel):
    """更新"""

    id: int | None = None
    lab_id: int | None = None
    name: str | None = None
    description: str | None = None
    img: str | None = None
    spec: str | None = None
    quantity: int | None = None
    status: int | None = None


class EquipmentDeleteRequest(BaseModel):
    """删"""

    id: int


class EquipmentPageRequest(BaseModel):
    """页面信息的请求"""

    lab_id: int | None = None
    page: int
    size: int
    keyword: str | None = None

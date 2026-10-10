from pydantic import BaseModel, ConfigDict


class ReservationCreateRequest(BaseModel):
    """预约记录请求"""

    lab_id: int
    equip_id: int | None = None
    date: str
    start_time: str
    end_time: str
    remark: str | None = None
    status: int

    model_config = ConfigDict(from_attributes=True)

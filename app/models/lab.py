import enum


from sqlalchemy import Integer, String

from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class LabStatus(enum.Enum):
    CLOSED = 0
    OPEN = 1


class Lab(Base):
    __tablename__ = "labs"
    __table_args__ = {"comment": "实验室信息表"}

    # str是强类型标注，在sqlalchemy中，类型标注决定了是否可以为Null，除非显式的加上nullable=True，才是可以为空的
    name: Mapped[str] = mapped_column(String(50), comment="实验室名称", nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), comment="描述")
    img: Mapped[str] = mapped_column(String(100), comment="封面", nullable=True)
    location: Mapped[str | None] = mapped_column(String(100), comment="位置")
    capacity: Mapped[int] = mapped_column(Integer, comment="容量", default=0)
    open_time: Mapped[str | None] = mapped_column(String(20), comment="开放时间")
    close_time: Mapped[str | None] = mapped_column(String(20), comment="关闭时间")
    status: Mapped[int] = mapped_column(
        Integer, comment="状态：0-禁用，1-正常", default=LabStatus.OPEN.value
    )

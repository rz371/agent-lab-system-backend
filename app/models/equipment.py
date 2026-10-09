import enum

from sqlalchemy import ForeignKey, Integer, String

from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.lab import Lab


class EquipStatus(enum.Enum):
    DISABLED = 0
    ENABLED = 1


class Equipment(Base):
    __tablename__ = "equipments"
    __table_args__ = {"comment": "设备信息表"}

    # 关联字段
    lab_id: Mapped[int] = mapped_column(
        # 关联的外键！表示 关联labs这个表的id ，这样两个表已经有关联了
        ForeignKey("labs.id"),
        comment="所属实验室",
        nullable=False,
    )

    name: Mapped[str] = mapped_column(String(50), comment="设备名称", nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), comment="描述")
    img: Mapped[str | None] = mapped_column(String(200), comment="封面")
    spec: Mapped[str | None] = mapped_column(String(100), comment="规格型号")
    quantity: Mapped[int] = mapped_column(Integer, comment="数量", default=1)
    status: Mapped[int] = mapped_column(
        Integer, comment="状态：0-禁用，1-正常", default=EquipStatus.ENABLED.value
    )

    # 有relationship 的话，从 设备这个模型，可以直接 .lab 就可以拿到 lab这个表的内容
    # 可以直接从lab这个表查到对应的内容
    lab: Mapped[Lab] = relationship()

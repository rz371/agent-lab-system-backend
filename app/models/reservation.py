import enum

from sqlalchemy import ForeignKey, Integer, String

from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.equipment import Equipment
from app.models.lab import Lab
from app.models.user import User


class ReserveStatus(enum.Enum):
    PENDING = 0
    APPROVED = 1
    REJECTED = 2
    CANCELED = 3


class Reservation(Base):
    __tablename__ = "reservations"
    __table_args__ = {"comment": "预约信息"}

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), comment="预约人", nullable=False
    )
    lab_id: Mapped[int] = mapped_column(
        ForeignKey("labs.id"), comment="实验室", nullable=False
    )
    equip_id: Mapped[int] = mapped_column(
        ForeignKey("equipments.id"), comment="设备，空表示预约实验室", nullable=True
    )
    date: Mapped[str] = mapped_column(String(20), comment="预约日期", nullable=False)
    start_time: Mapped[str] = mapped_column(
        String(20), comment="开始时间", nullable=False
    )
    end_time: Mapped[str] = mapped_column(
        String(20), comment="结束时间", nullable=False
    )
    remark: Mapped[str] = mapped_column(String(255), comment="备注")
    status: Mapped[int] = mapped_column(
        Integer,
        comment="预约状态，0：待审核；1：已通过；2：已拒绝；3：已取消",
        default=ReserveStatus.PENDING.value,
    )

    lab: Mapped[Lab] = relationship()
    equip: Mapped[Equipment] = relationship()
    user: Mapped[User] = relationship()

from datetime import datetime

from sqlalchemy.orm import Session


from app.common.exceptions import BusinessException
from app.models.equipment import Equipment
from app.models.lab import Lab
from app.models.reservation import Reservation
from app.models.user import User
from app.schemas.reservation import ReservationCreateRequest


def creater_eservation(db: Session, current_user: User, data: ReservationCreateRequest):
    """
    新增预约记录
    -- 预约的日期不可以小于当前日期
    -- 预约的时间不可小于当前时间
    -- 实验室是否被预约
    -- 该实验室下的设备是否被人预约
    -- 实验室/设备 是否可用 （不是禁用）
    """
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M")
    if data.date < current_date:
        raise BusinessException(message="预约日期不可小于当前日期")
    if data.end_time < data.start_time:
        raise BusinessException(message="预约起始时间不可大于结束时间")
    if data.date == current_date and data.start_time < current_time:
        raise BusinessException(message="预约开始时间不可小于当前时间")

    lab = db.query(Lab).filter(data.lab_id == Lab.id).first()
    if not lab:
        raise BusinessException(message="该实验室不存在")
    if lab.status != 1:
        raise BusinessException(message="该实验室已关闭")

    if lab.open_time and data.start_time < lab.open_time:
        raise BusinessException(message="预约的开始时间不可早于实验室开放时间")
    if lab.close_time and data.end_time > lab.close_time:
        raise BusinessException(message="预约的结束时间不可晚于实验室开放时间")

    if data.equip_id:  # 有设备id，表示要预约实验室的设备了
        equip = db.query(Equipment).filter(Equipment.id == data.equip_id).first()
        if not equip:
            raise BusinessException(message="该实验室设备不存在")
        if equip.status != 1:
            raise BusinessException(message="该实验室设备正在维修中")

    # 查看实验室/设备是否是预约 状态
    # 因为这个可以实验室和设备分开预约
    query = db.query(Reservation).filter(
        data.lab_id == Reservation.lab_id,  # 是不是同一个实验室
        data.date == Reservation.date,  # 是不是同一天
        data.start_time < Reservation.end_time,  # 时间重叠
        data.end_time > Reservation.start_time,
        Reservation.status.in_([0, 1]),  # 记录状态里面的01都作数，都可以是占用
    )
    if data.equip_id:
        query = query.filter(Reservation.equip_id == data.equip_id)  # 预约了设备
    else:
        query = query.filter(Reservation.equip_id.is_(None))  # 只预约了实验室
    if query.first():
        raise BusinessException(message="该时段已经预约")
    #
    reservation_model = Reservation(
        # **data.model_dump(), user_id=current_user.id, status=0
        user_id=current_user.id,
        lab_id=data.lab_id,
        equip_id=data.equip_id,
        date=data.date,
        start_time=data.start_time,
        end_time=data.end_time,
        remark=data.remark,
        status=0,
    )
    db.add(reservation_model)
    db.commit()
    # db.refresh()
    return "新增成功"
    # if reserva and reserva.start_time > data.start_time:
    #     raise BusinessException(message='该实验室已被预约')
    # # db.query(Reservation).filter(data.date > current_date).first()

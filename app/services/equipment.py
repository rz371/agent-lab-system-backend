from operator import or_

from sqlalchemy.orm import Session

from app.common.exceptions import BusinessException
from app.common.response import pageResponse
from app.models.equipment import Equipment
from app.models.lab import Lab
from app.schemas.equipment import (
    EquipmentCreateRequest,
    EquipmentDeleteRequest,
    EquipmentPageRequest,
    EquipmentResponse,
    EquipmentUpdateRequest,
)


def get_equipment_manager_all(data: EquipmentPageRequest, db: Session):
    """查条件下的数据"""
    query = db.query(Equipment)
    if data.lab_id:
        query = query.filter(Equipment.lab_id == data.lab_id)
    if data.keyword:
        query = query.filter(Equipment.name.like(f"%{data.keyword}%"))

    total = query.count()

    items = (
        query.order_by(Equipment.id.asc())
        .offset((data.page - 1) * data.size)
        .limit(data.size)
        .all()
    )
    print("33", items)
    result = []
    for item in items:
        # 可以写EquipmentResponse.model_validate 这个前提是
        # EquipmentResponse里面写了from_attributes=True
        # 否则报错
        val = EquipmentResponse.model_validate(item)
        val.lab_name = item.lab.name if item.lab else None
        result.append(val)

    return pageResponse(total=total, list=result)


def create_equipment(data: EquipmentCreateRequest, db: Session):
    """新增设备"""
    lab = db.query(Lab).filter(Lab.id == data.lab_id).first()
    if not lab:
        raise BusinessException(message="所属实验室不存在")
    exist = (
        db.query(Equipment)
        .filter(
            # 同一实验室的设备不能重名
            Equipment.name == data.name,
            Equipment.lab_id == data.lab_id,
        )
        .first()
    )
    if exist:
        raise BusinessException(message="该设备已存在")

    equip = Equipment(**data.model_dump(exclude_none=True))
    db.add(equip)
    db.commit()
    db.refresh(equip)
    val = EquipmentResponse.model_validate(equip)
    val.lab_name = equip.lab.name if equip.lab else None
    return val


def update_equipment(data: EquipmentUpdateRequest, db: Session):
    """更新"""
    equip = db.query(Equipment).filter(Equipment.id == data.id).first()
    if not equip:
        raise BusinessException(message="该设备不存在")

    payload = data.model_dump(exclude_none=True)
    # 判断payload改lab_id 就拿lab_id ，没有改的话，就拿equip.lab_id
    lab_id = payload.get("lab_id", equip.lab_id)
    name = payload.get("name", equip.name)
    lab = db.query(Lab).filter(Lab.id == lab_id).first()
    if not lab:
        raise BusinessException(message="实验室不存在")

    exist = (
        db.query(Equipment)
        .filter(
            Equipment.lab_id == lab_id,  # 同一个实验室
            Equipment.name == name,  # 同一个名称
            Equipment.id != equip.id,  # 把我自己排除掉，看看还有没有和我重名的了
        )
        .first()
    )
    if exist:
        raise BusinessException(message="同一个实验室设备不可以重名")

    for key, value in payload.items():
        setattr(equip, key, value)

    db.commit()
    db.refresh(equip)
    val = EquipmentResponse.model_validate(equip)
    val.lab_name = equip.lab.name if equip.lab else None
    return val


def delete_equipment(data: EquipmentDeleteRequest, db: Session):
    exist = db.query(Equipment).filter(Equipment.id == data.id).first()
    if not exist:
        raise BusinessException(message="设备不存在")

    db.delete(exist)
    db.commit()
    return "删除成功"

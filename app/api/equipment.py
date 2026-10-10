from fastapi import APIRouter, Depends

from app.common.response import Response
from app.database import get_db
from app.dependencies.auth import get_current_admin, get_current_user
from app.models.equipment import Equipment
from app.schemas.equipment import (
    EquipmentCreateRequest,
    EquipmentDeleteRequest,
    EquipmentPageRequest,
    EquipmentUpdateRequest,
)
from sqlalchemy.orm import Session

from app.services import equipment

router = APIRouter(prefix="/equip", tags=["实验室设备信息接口"])


@router.get("/info")
def get_equip_info(
    data: EquipmentPageRequest = Depends(),
    # 学生身份也可以访问这个
    current_user: Equipment = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取设备信息"""
    res = equipment.get_equipment_manager_all(data, db)
    return Response.success(data=res)


@router.post("/create")
def create_equip(
    data: EquipmentCreateRequest,
    current_user: Equipment = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """增"""
    res = equipment.create_equipment(data, db)
    return Response.success(data=res)


@router.post("/update")
def update_equip(
    data: EquipmentUpdateRequest,
    current_user: Equipment = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """更新"""
    res = equipment.update_equipment(data, db)
    return Response.success(data=res)


@router.post("/delete")
def delete_equip(
    data: EquipmentDeleteRequest,
    current_user: Equipment = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """删除"""
    equipment.delete_equipment(data, db)
    return Response.success()


@router.get("/desc/{lab_id}")
def desc_equip(
    lab_id: int,
    page: int,
    size: int,
    # data: EquipmentPageRequest = Depends(),
    current_user: Equipment = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    res = equipment.desc_equipment(lab_id, page, size, db)
    return Response.success(data=res)

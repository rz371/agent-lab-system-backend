from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.common.response import Response
from app.database import get_db
from app.dependencies.auth import get_current_admin
from app.models.lab import Lab
from app.schemas.lab import (
    LabCreateRequest,
    LabDeleteRequest,
    LabPageRequest,
    LabUpdateRequest,
)
from app.services import lab as lab_service

router = APIRouter(prefix="/lab", tags=["实验室管理"])


@router.get("/info")
def get_lab_info(
    data: LabPageRequest = Depends(),
    current_user: Lab = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """获取实验室信息"""
    res = lab_service.get_lab_manager_all(data, db)
    return Response.success(data=res)


@router.post("/create")
def create_lab(
    data: LabCreateRequest,
    current_user: Lab = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """新增实验室"""
    res = lab_service.create_lab(data, db)
    return Response.success(data=res)


@router.post("/update")
def update_lab(
    data: LabUpdateRequest,
    current_user: Lab = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """编辑实验室"""
    res = lab_service.update_lab(data, db)
    return Response.success(message="编辑成功", data=res)


@router.post("/delete")
def delete_lab(
    data: LabDeleteRequest,
    current_user: Lab = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """删除实验室"""
    lab_service.delete_lab(data, db)
    return Response.success(message="删除成功")

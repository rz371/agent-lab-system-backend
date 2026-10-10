from operator import or_

from app.common.exceptions import BusinessException
from app.common.response import pageResponse
from app.models.lab import Lab
from app.schemas.lab import (
    LabCreateRequest,
    LabDeleteRequest,
    LabDescRequest,
    LabPageRequest,
    LabResponse,
    LabUpdateRequest,
)
from sqlalchemy.orm import Session


def get_lab_manager_all(data: LabPageRequest, db: Session):
    """获取实验室所有信息"""

    query = db.query(Lab)
    if data.keyword:
        query = query.filter(Lab.name.ilike(f"%{data.keyword}%"))

    total = query.count()

    items = (
        query.order_by(Lab.id.desc())
        .offset((data.page - 1) * data.size)
        .limit(data.size)
        .all()
    )

    # items 结果是一个orm对象，需要变为JSON
    return pageResponse(
        total=total, list=[LabResponse.model_validate(item) for item in items]
    )


def create_lab(data: LabCreateRequest, db: Session):
    """新增实验室"""
    print(data)
    print("*" * 20)
    print(Lab.name)
    exist = db.query(Lab).filter(Lab.name == data.name).first()

    if exist:
        raise BusinessException(message="实验室已存在")

    lab = Lab(**data.model_dump(exclude_none=True))
    db.add(lab)
    db.commit()
    db.refresh(lab)
    return LabResponse.model_validate(lab)


def update_lab(data: LabUpdateRequest, db: Session):
    """编辑实验室"""
    lab = db.query(Lab).filter(Lab.id == data.lab_id).first()
    if not lab:
        raise BusinessException(message="实验室不存在")

    items = data.model_dump(exclude_none=True)
    for key, value in items.items():
        setattr(lab, key, value)

    db.commit()
    db.refresh(lab)
    return LabResponse.model_validate(lab)


def delete_lab(data: LabDeleteRequest, db: Session):
    """删除实验室"""
    exist = db.query(Lab).filter(Lab.id == data.lab_id).first()
    if not exist:
        raise BusinessException(message="实验室不存在")

    db.delete(exist)
    db.commit()
    return "已成功删除"


def desc_lab(lab_id: int, db: Session):
    """通过实验室id获取实验室详情数据"""
    lab = db.query(Lab).filter(Lab.id == lab_id).first()
    if not lab:
        raise BusinessException(message="该实验室不存在")

    return LabResponse.model_validate(lab)

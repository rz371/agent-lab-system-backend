from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.common.response import Response
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreateRequest
from app.services import reservation

router = APIRouter(prefix="/reservation", tags=["预约"])


@router.post("/create")
def create_reser(
    data: ReservationCreateRequest,
    db: Session = Depends(get_db),
    current_user: Reservation = Depends(get_current_user),
):
    reservation.creater_eservation(db, current_user, data)
    return Response.success(message="新增成功")

from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session

from schemas import ExcursionReservationSchema
from db.config import get_db
import db.crud.excursion_reservation_crud as crud


router = APIRouter(prefix="/excursion_reservation", tags=["excursion_reservation"])


@router.get("/list")
async def list_excursion_reservation(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_excursion_reservation(db, skip, limit)
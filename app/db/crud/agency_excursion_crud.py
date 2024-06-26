from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import AgencyExcursionAssociation, ExcursionModel
from schemas import AgencyExcursionAssociationSchema
from db.crud.agency_crud import get_agency
from db.crud.excursion_crud import get_excursion


def list_agency_excursion(db: Session, skip: int, limit: int):
    return db.query(AgencyExcursionAssociation).offset(skip).limit(limit).all()


def get_agency_excursion(db: Session, agency_id: int, excursion_id: int):
    return db.query(AgencyExcursionAssociation).filter(AgencyExcursionAssociation.agency_id == agency_id, AgencyExcursionAssociation.excursion_id == excursion_id).first()

def get_agency_excursion_by_excursion(db: Session, excursion_id: int):
    return db.query(AgencyExcursionAssociation).filter(AgencyExcursionAssociation.excursion_id == excursion_id).first()

def create_agency_excursion(db: Session, agency_excursion_create: AgencyExcursionAssociation):

    agency = get_agency(db, agency_excursion_create.agency_id)
    if agency is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found")
    
    excursion = get_excursion(db, agency_excursion_create.excursion_id)
    if excursion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Excursion not found")
    
    agency_excursion = get_agency_excursion(db, agency_excursion_create.agency_id, agency_excursion_create.excursion_id)
    if agency_excursion is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Agency excursion already exists")

    agency_excursion = toModel(agency_excursion_create)
    db.add(agency_excursion)
    db.commit()
    db.refresh(agency_excursion)

    return "Success"

def delete_agency_excursion(db: Session, agency_id: int, excursion_id: int):


    agency = get_agency(db, agency_id)
    if agency is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found")
    
    excursion = get_excursion(db, excursion_id)
    if excursion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Excursion not found")
    
    agency_excursion = get_agency_excursion(db, agency_id, excursion_id)
    if agency_excursion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency excursion association not found")

    db.delete(agency_excursion)
    db.commit()

    return "Success"


def get_weekend_excursions(db:Session, agency_id:int):
    agency = get_agency(db, agency_id)
    if agency is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found")
    
    related_excursions = db.query(
        ExcursionModel
        ).join(
            AgencyExcursionAssociation
        ).filter(
            AgencyExcursionAssociation.agency_id == agency_id
        ).filter(
            ExcursionModel.departure_day.in_(["Friday", "Saturday", "Sunday", "Viernes", "Sábado", "Domingo"])
        ).all()

    return related_excursions


def toModel(schema:AgencyExcursionAssociationSchema) -> AgencyExcursionAssociation:
    return AgencyExcursionAssociation(agency_id=schema.agency_id,
                                      excursion_id=schema.excursion_id)

def toShema(model:AgencyExcursionAssociation) -> AgencyExcursionAssociationSchema:
    return AgencyExcursionAssociationSchema(agency_id=model.agency_id,
                                            excursion_id=model.excursion_id)
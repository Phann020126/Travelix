from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlalchemy.orm import Session
from models import AgencyModel, PackageReservation, AgencyExcursionAssociation, ExcursionReservation, AgencyOfferAssociation, PackageModel
from schemas import AgencySchema
# from db.crud.package_reservation_crud import get_package_reservation_by_agency
# from db.crud.agency_excursion_crud import get_agency_excursion_by_agency
# from db.crud.excursion_reservation_crud import get_excursion_reservation_by_excursion



def list_agency(db: Session, skip: int, limit: int):
    return db.query(AgencyModel).offset(skip).limit(limit).all()

def get_agency(db: Session, id: int):
    return db.query(AgencyModel).filter(AgencyModel.id == id).first()

def create_agency(db: Session, agency_create: AgencySchema):
    agency = toModel(agency_create)
    db.add(agency)
    db.commit()
    db.refresh(agency)

    return "Success"

def delete_agency(db: Session, agency_delete: AgencySchema):

    agency = get_agency(db, agency_delete.id)

    if agency is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found")
    

    db.delete(agency)
    db.commit()

    return "Success"

def update_agency(db: Session, agency_update: AgencySchema):

    agency = get_agency(db, agency_update.id)

    if agency is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found")
    
    agency_in_package_reservation = db.query(PackageReservation).filter(PackageReservation.agency_id == agency_update.id).first()
    # agency_in_package_reservation = get_package_reservation_by_agency(db, agency_update.id)

    if agency_in_package_reservation is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't update this agency because is is ivolved in a Package Reservation")
    
    excursions_associated_with_agency = db.query(AgencyExcursionAssociation).filter(AgencyExcursionAssociation.agency_id == agency_update.id).all()
    # excursions_associated_with_agency = get_agency_excursion_by_agency(db, agency_update.id)

    for excursion in excursions_associated_with_agency:
        excursion_reservation = db.query(ExcursionReservation).filter(ExcursionReservation.excursion_id == excursion.excursion_id).first()
        # excursion_reservation = get_excursion_reservation_by_excursion(db, excursion.excursion_id)
        if excursion_reservation is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't update this agency because is is ivolved in an Excursion Reservation")
    
    if agency_update.name is not None:
        agency.name = agency_update.name
    if agency_update.address is not None:
        agency.address = agency_update.address
    if agency_update.fax_number is not None:
        agency.fax_number = agency_update.fax_number
    if agency_update.email is not None:
        agency.email = agency_update.email
    if agency_update.photo_url is not None:
        agency.photo_url = agency_update.photo_url

    db.commit()

    return "Success"

def toModel(schema:AgencySchema) -> AgencyModel:
    return AgencyModel(
        # id=schema.id, 
                       name=schema.name, 
                       address=schema.address, 
                       fax_number=schema.fax_number, 
                       email=schema.email,
                       photo_url=schema.photo_url)

def toShema(model:AgencyModel) -> AgencySchema:
    return AgencySchema(id=model.id, 
                        name=model.name, 
                        address=model.address, 
                        fax_number=model.fax_number, 
                        email=model.email,
                        photo_url=model.photo_url)

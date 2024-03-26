from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlalchemy.orm import Session
from models import OfferModel, AgencyOfferAssociation
from schemas import OfferSchema
import db.crud.hotel_crud as hotel



def list_offer(db: Session, skip: int, limit: int):
    return db.query(OfferModel).offset(skip).limit(limit).all()

def get_offer(db: Session, id: int):
    return db.query(OfferModel).filter(OfferModel.id == id).first()

def create_offer(db: Session, offer_create: OfferSchema):
    hotel_exists = hotel.get_hotel(db, offer_create.hotel_id)

    if hotel_exists is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hotel does not exist",
        )
    
    offer = toModel(offer_create)
    db.add(offer)
    db.commit()
    db.refresh(offer)

    return "Success"


def delete_offer(db: Session, offer_delete: OfferSchema):

    offer = get_offer(db, offer_delete.id)

    if offer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Offer not found")
    
    db.delete(offer)
    db.commit()

    return "Success"

def toModel(schema:OfferSchema) -> OfferModel:
    return OfferModel(
        # id=schema.id,
                          price=schema.price,
                          description=schema.description,
                          hotel_id=schema.hotel_id)

def toShema(model:OfferModel) -> OfferSchema:
    return OfferSchema(id=model.id, 
                           price=model.price,
                           description=model.description,
                           hotel_id=model.hotel_id)
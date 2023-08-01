from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.database.models import Photo, User, Estimate
from src.repository.photos import get_record
from src.services.role import role_service
from src.constants import *


async def is_exists_estimate(photo_id: str, user: User, db: Session):
    estimate = (
        db.query(Estimate)
        .filter(and_(Estimate.photo_id == photo_id, Estimate.user_id == user.id))
        .first()
    )
    return bool(estimate)


async def get_estimates(photo_id: str, db: Session) -> List[Estimate]:
    estimates = [est.estimate for est in db.query(Estimate).filter(Estimate.photo_id == photo_id).all()]
    return estimates or None


async def estimate_photo(photo_id: str, estimate: int, user: User, db: Session) -> Estimate:
    photo = await get_record(photo_id, Photo, db)
    is_exists = await is_exists_estimate(photo_id, user, db)
    if photo is None or photo.user_id == user.id or is_exists:
        return None
    new_estimate = Estimate(estimate=estimate, photo_id=photo_id, user_id=user.id)
    current_estimates = await get_estimates(photo_id, db) or list()
    current_estimates.append(new_estimate.estimate)
    rating = sum(current_estimates) / len(current_estimates)
    photo.rating = rating
    db.add(photo)
    db.commit()
    db.refresh(photo)

    db.add(new_estimate)
    db.commit()
    db.refresh(new_estimate)

    return new_estimate


async def delete_estimate(estimate_id: str, user: User, db: Session) -> Estimate:
    estimate = db.query(Estimate).filter(Estimate.id == estimate_id).first()
    if estimate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ESTIMATE_NOT_FOUND)
    photo = db.query(Photo).filter(Photo.id == estimate.photo_id).first()
    if estimate.user_id == user.id or await role_service.is_admin(user):
        db.delete(estimate)
        db.commit()
        estimates = await get_estimates(photo.id, db)
        rating = 0
        if estimates is not None:
            rating = sum(estimates) / len(estimates)
        photo.rating = rating
        db.add(photo)
        db.commit()
        db.refresh(photo)
    return estimate


async def get_photo_estimates(photo_id: str, db: Session) -> List[Estimate]:
    estimates = [est for est in db.query(Estimate).filter(Estimate.photo_id == photo_id).all()]
    return estimates or None
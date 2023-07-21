from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Photo, User, Estimate
from src.repository.photos import get_record
from src.messages import *


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
    raiting = sum(current_estimates) / len(current_estimates)
    photo.raiting = raiting
    db.add(new_estimate)
    db.add(photo)
    db.commit()
    db.refresh(new_estimate)
    db.refresh(photo)
    return new_estimate


async def delete_estimate(estimate_id: str, user: User, db: Session) -> Estimate:
    estimate = db.query(Estimate).filter(Estimate.id == estimate_id).first()
    photo = db.query(Photo).filter(Photo.id == estimate.photo_id).first()
    if estimate and estimate.user_id == user.id:
        db.delete(estimate)
        db.commit()
        estimates = await get_estimates(photo.id, db)
        raiting = sum(estimates) / len(estimates)
        photo.raiting = raiting
        db.add(photo)
        db.commit()
        db.refresh(photo)
    return estimate
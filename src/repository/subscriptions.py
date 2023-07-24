from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status

from src.database.models import User, Subscription
from src.messages import *


async def subscribe(author_id: str, user: User, db: Session) -> Subscription:
    author = db.query(User).filter(User.id == author_id).first()
    if author:
        subscription = Subscription(subscriber_id = user.id, author_id = author_id)
        db.add(subscription)
        db.commit()
        db.refresh(subscription)
        return subscription
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = USER_ID_NOT_FOUND)


async def get_subscriptions(user: User, db: Session) -> List[Subscription]:
    subscriptions = db.query(Subscription).filter(Subscription.subscriber_id == user.id).all()
    return subscriptions


async def unsubscribe(subscription_id: str, user: User, db: Session) -> Subscription:
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if subscription:
        db.delete(subscription)
        db.commit()
    return subscription


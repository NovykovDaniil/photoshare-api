from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.database.models import User, Subscription
from src.constants import *


async def subscribe(author_id: str, user: User, db: Session) -> Subscription:
    author = db.query(User).filter(User.id == author_id).first()
    if author:
        subscription = Subscription(subscriber_id = user.id, author_id = author_id)
        user.subscriptions += 1
        author.subscribers += 1
        db.add(subscription)
        db.commit()
        db.refresh(subscription)
        db.commit()
        return subscription
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = USER_ID_NOT_FOUND)


async def get_subscriptions(user: User, db: Session) -> List[Subscription]:
    subscriptions = db.query(Subscription).filter(Subscription.subscriber_id == user.id).all()
    return subscriptions


async def unsubscribe(subscription_id: str, user: User, db: Session) -> Subscription:
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if subscription:
        author = db.query(User).filter(User.id == subscription.author_id).first()
        if author:
            author.subscribers -= 1
            user.subscriptions -= 1
            db.delete(subscription)
            db.commit()
            db.commit() 
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=AUTHOR_ID_NOT_FOUND)
    return subscription

from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    status,
    UploadFile,
    File,
    Form,
    HTTPException,
    status,
    Query,
)
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import (
    SubscriptionResponse,
    SubscriptionsResponse,
)
from src.database.models import User
from src.repository import subscriptions as repository_subscriptions
from src.services.auth import token_service
from src.messages import *


router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@router.get('/', response_model=SubscriptionsResponse)
async def get_subscriptions(user: User = Depends(token_service.get_current_user), db: Session = Depends(get_db)):
    subscriptions = await repository_subscriptions.get_subscriptions(user, db)
    if not subscriptions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = SUBS_NOT_FOUND)
    return {'subscriptions': subscriptions, 'detail': SUBS_FOUND}


@router.post('/{author_id}', response_model=SubscriptionResponse)
async def subscribe(author_id: str, user: User = Depends(token_service.get_current_user), db: Session = Depends(get_db)):
    subscription = await repository_subscriptions.subscribe(author_id, user, db)
    return {'subscription': subscription, 'detail': SUBSCRIBED}


@router.delete('/{subscription_id}', response_model=SubscriptionResponse)
async def unsubscribe(subscription_id: str, user: User = Depends(token_service.get_current_user), db: Session = Depends(get_db)):
    subscription = await repository_subscriptions.unsubscribe(subscription_id, user, db)
    if subscription is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_SUB)
    return {'subscription': subscription, 'detail': SUB_DELETED}
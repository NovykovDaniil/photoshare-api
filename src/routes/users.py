from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import UserResponse, UserEditModel, UserBanModel
from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import token_service
from src.messages import *


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{username}", response_model=UserResponse)
async def get_user(username: str, db: Session = Depends(get_db)):
    user = await repository_users.get_user(username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_USERNAME)
    return {"user": user, "detail": USER_FOUND}


@router.put("/{username}/edit", response_model=UserResponse)
async def edit_user(
    body: UserEditModel,
    user: User = Depends(token_service.get_current_user),
    db: Session = Depends(get_db),
):
    user_ = await repository_users.edit_user(body.username, body.bio, user, db)
    if user_ is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_USERNAME)
    return {"user": user_, "detail": USER_EDITED}


@router.put("/{username}/active", response_model=UserResponse)
async def ban_user(
    body: UserBanModel,
    user: User = Depends(token_service.get_current_user),
    db: Session = Depends(get_db),
):
    user_ = await repository_users.change_user_active(body.username, user, db)
    return {"user": user_, "detail": USER_ACTIVE_CHANGED}

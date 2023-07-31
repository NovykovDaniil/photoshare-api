from fastapi import (
    APIRouter,
    Depends,
    status,
    UploadFile,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import (
    MessageModel,
    MessageResponse,
    MessageEditModel,
)
from src.database.models import User
from src.repository import messages as repository_messages
from src.services.auth import token_service
from src.constants import *


router = APIRouter(prefix="/messages", tags=["messages"])


@router.post('/', response_model=MessageResponse)
async def create_message(body: MessageModel, user: User = Depends(token_service.get_current_user), db: Session = Depends(get_db)):
    message = await repository_messages.create_message(body.chat_id, body.text, user, db)
    return {'message': message, 'detail': MESSAGE_CREATED}


@router.put('/{message_id}', response_model=MessageResponse)
async def edit_message(body: MessageEditModel, user: User = Depends(token_service.get_current_user), db: Session = Depends(get_db)):
    message = await repository_messages.edit_message(body.message_id, body.text, user, db)
    return {'message': message, 'detail': MESSAGE_EDITED}


@router.delete('/{message_id}', response_model=MessageResponse)
async def delete_message(message_id: str, user: User = Depends(token_service.get_current_user), db: Session = Depends(get_db)):
    message = await repository_messages.delete_message(message_id, user, db)
    return {'message': message, 'detail': MESSAGE_DELETED}


@router.get('/{message_id}', response_model=MessageResponse)
async def get_message(message_id: str, user: User = Depends(token_service.get_current_user), db: Session = Depends(get_db)):
    message = await repository_messages.get_message(message_id, user, db)
    return {'message': message, 'detail': MESSAGE_FOUND}


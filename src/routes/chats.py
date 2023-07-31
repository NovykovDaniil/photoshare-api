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
    ChatModel,
    ChatResponse,
    MessagesResponse,
)
from src.database.models import User
from src.repository import chats as repository_chats
from src.services.auth import token_service
from src.constants import *


router = APIRouter(prefix="/chats", tags=["chats"])


@router.post('/', response_model=ChatResponse)
async def create_chat(body: ChatModel, user: User = Depends(token_service.get_current_user), db: Session = Depends(get_db)):
    chat = await repository_chats.create_chat(body.interlocutor_id, user, db)
    if chat is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=CHAT_EXISTS)
    return {'chat': chat, 'detail': CHAT_CREATED}


@router.delete('/{chat_id}', response_model=ChatResponse)
async def delete_chat(chat_id: str, user: User = Depends(token_service.get_current_user), db: Session = Depends(get_db)):
    chat = await repository_chats.delete_chat(chat_id, user, db)
    return {'chat': chat, 'detail': CHAT_DELETED}


@router.get('/{chat_id}', response_model=ChatResponse)
async def get_chat(chat_id: str, user: User = Depends(token_service.get_current_user), db: Session = Depends(get_db)):
    chat = await repository_chats.get_chat(chat_id, user, db)
    return {'chat': chat, 'detail': CHAT_FOUND}


@router.get('/{chat_id}/messages', response_model=MessagesResponse)
async def get_messages(chat_id: str, user: User = Depends(token_service.get_current_user), db: Session = Depends(get_db)):
    messages = await repository_chats.get_messages(chat_id, user, db)
    return {'messages': messages, 'detail': MESSAGES_FOUND}

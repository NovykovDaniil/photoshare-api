from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from fastapi import HTTPException, status

from src.database.models import User, Chat, Message
from src.services.role import role_service
from src.messages import *


async def create_chat(interlocutor_id: str, user: User, db: Session):
    chat = (
        db.query(Chat)
        .filter(
            or_(
                and_(
                    Chat.interlocutor_1 == user.id,
                    Chat.interlocutor_2 == interlocutor_id,
                ),
                and_(
                    Chat.interlocutor_1 == interlocutor_id,
                    Chat.interlocutor_2 == user.id,
                ),
            )
        )
        .first()
    )

    interlocutor = db.query(User).filter(User.id == interlocutor_id).first()
    if interlocutor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_ID_NOT_FOUND)

    if chat is None:
        chat = Chat(interlocutor_1=user.id, interlocutor_2=interlocutor_id)
        db.add(chat)
        db.commit()
        db.refresh(chat)

    return chat


async def delete_chat(chat_id: str, user: User, db: Session):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = CHAT_DOES_NOT_EXISTS)
    if chat.interlocutor_1 == user.id or chat.interlocutor_2 == user.id or await role_service.is_admin(user):
        db.delete(chat)
        db.commit()
        return chat
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=NO_PERMISSIONS)


async def get_chat(chat_id: str, user: User, db: Session):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = CHAT_NOT_FOUND)
    if chat.interlocutor_1 == user.id or chat.interlocutor_2 == user.id or await role_service.is_admin(user):
        return chat
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=NO_PERMISSIONS)
    

async def get_messages(chat_id: str, user: User, db: Session) -> List[Message]:
    chat = await get_chat(chat_id, user, db)
    messages = chat.messages
    if not messages:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_MESSAGES)
    return messages
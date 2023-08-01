from datetime import datetime

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.database.models import User, Message, Chat
from src.services.role import role_service
from src.constants import *


async def create_message(chat_id: str, text: str, user: User, db: Session) -> Message:
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = CHAT_NOT_FOUND)
    if chat.interlocutor_1 == user.id or chat.interlocutor_2 == user.id:
        recipient = chat.interlocutor_1 if chat.interlocutor_1 != user.id else chat.interlocutor_2
        message = Message(sender=user.id, recipient=recipient, text=text)
        chat.messages.append(message)
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=NO_PERMISSIONS)


async def get_message(message_id: str, user: User, db: Session) -> Message:
    message = db.query(Message).filter(Message.id == message_id).first()
    if message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=MESSAGE_DOES_NOT_EXIST)
    if message.sender == user.id or await role_service.is_moder(user):
        return message
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=NO_PERMISSIONS)


async def edit_message(message_id: str, text: str, user: User, db: Session) -> Message:
    message = await get_message(message_id, user, db)
    message.text = text
    message.updated_at = datetime.utcnow()
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


async def delete_message(message_id: str, user: User, db: Session) -> Message:
    message = await get_message(message_id, user, db)
    db.delete(message)
    db.commit()
    return message


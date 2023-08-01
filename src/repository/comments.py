from typing import List
from datetime import datetime

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.database.models import Photo, User, Comment
from src.repository.photos import get_record, verify_record
from src.constants import *


async def create_comment(photo_id: str, text: str, user: User, db: Session) -> Comment:
    photo = await get_record(photo_id, Photo, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_PHOTO)
    comment = Comment(text=text, photo_id=photo_id, user_id=user.id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


async def edit_comment(comment_id: str, new_text: str, user: User, db: Session) -> Comment:
    comment = await verify_record(comment_id, Comment, user, db)
    comment.text, comment.updated_at = new_text, datetime.utcnow()
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


async def delete_comment(comment_id: str, user: User, db: Session) -> Comment:
    comment = await verify_record(comment_id, Comment, user, db)
    if comment:
        db.delete(comment)
        db.commit()
    return comment


async def get_comments(photo_id: str, db: Session) -> List[Comment]:
    comments = db.query(Comment).filter(Comment.photo_id == photo_id).all()
    return comments
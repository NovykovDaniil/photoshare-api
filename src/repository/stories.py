from datetime import datetime
from typing import List

from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status

from src.database.models import User, Story, Subscription
from src.services.photos import UploadService
from src.services.role import role_service
from src.messages import *


async def verify_story(story: Story, user: User) -> bool:
    if story.user_id == user.id or role_service.is_moder(user):
        return True
    return False


async def get_story(story_id: str, db: Session) -> Story:
    story = db.query(Story).filter(Story.id == story_id).first()
    if story.expire_to > datetime.utcnow():
        return story
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=STORY_NOT_AVALIABLE)


async def create_story(file: UploadFile, user: User, db: Session) -> Story:
    if file.content_type.split("/")[0] != "video":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ONLY_VIDEO,
        )

    public_id = UploadService.create_name(user.email, "RestAPI")
    r = UploadService.upload_video(file.file, public_id)

    url = UploadService.get_video_url(public_id, r.get("version"))

    story = Story(url = url, user_id = user.id)

    db.add(story)
    db.commit()
    db.refresh(story)

    return story


async def delete_story(story_id: str, user: User, db: Session) -> Story:
    story = await get_story(story_id, db)
    if story:
        is_owner = await verify_story(story, user)
        if not is_owner:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = STORY_NOT_YOUR)
        db.delete(story)
        db.commit()
    return story


async def recommend(user: User, db: Session) -> List[Story]:
    stories = []
    authors_id = [subscription.author_id for subscription in db.query(Subscription).filter(Subscription.subscriber_id == user.id).all()]
    for author_id in authors_id:
        stories.extend([story for story in db.query(Story).filter(Story.user_id == author_id)])
    return stories
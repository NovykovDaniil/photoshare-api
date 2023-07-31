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
    StoryResponse,
    StoriesResponse,
)
from src.database.models import User
from src.repository import stories as repository_stories
from src.services.auth import token_service
from src.constants import *


router = APIRouter(prefix="/stories", tags=["stories"])


@router.post('/', response_model=StoryResponse)
async def create_story(file: UploadFile, user: User = Depends(token_service.get_current_user), db: Session = Depends(get_db)):
    story = await repository_stories.create_story(file, user, db)
    return {'story': story, 'detail': STORY_CREATED}


@router.delete('/{story_id}', response_model=StoryResponse)
async def delete_story(story_id: str, user: User = Depends(token_service.get_current_user), db: Session = Depends(get_db)):
    story = await repository_stories.delete_story(story_id, user, db)
    if story is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_STORY)
    return {'story': story, 'detail': STORY_DELETED}


@router.get('/{story_id}', response_model=StoryResponse)
async def get_story(story_id: str, db: Session = Depends(get_db)):
    story = await repository_stories.get_story(story_id, db)
    if story is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_STORY)
    return {'story': story, 'detail': STORY_FOUND}


@router.get('/', response_model=StoriesResponse)
async def recommend(user: User = Depends(token_service.get_current_user), db: Session = Depends(get_db)):
    stories = await repository_stories.recommend(user, db)
    if not stories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_STORIES)
    return {'stories': stories, 'detail': STORIES_FOUND}

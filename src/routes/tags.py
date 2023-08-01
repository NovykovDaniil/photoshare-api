from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status,
)
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import TagModel, TagResponse
from src.database.models import Tag
from src.repository import tags as repository_tags
from src.constants import TAG_EXISTS, TAG_CREATED


router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(body: TagModel, db: Session = Depends(get_db)) -> Tag:
    if await repository_tags.is_exists(body, db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=TAG_EXISTS)
    new_tag = await repository_tags.create_tag(body, db)
    return {"tag": new_tag, "details": TAG_CREATED}
from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import (
    CommentModel,
    CommentResponse,
    CommentsResponse,
    CommentEditModel,
    CommentHandleModel,
)
from src.database.models import User
from src.repository import comments as repository_comments
from src.services.auth import token_service
from src.constants import *


router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/{photo_id}", response_model=CommentResponse)
async def create_comment(
    body: CommentModel,
    user: User = Depends(token_service.get_current_user),
    db: Session = Depends(get_db),
):
    comment = await repository_comments.create_comment(
        body.photo_id, body.text, user, db
    )
    return {"comment": comment, "detail": COMMENT_CREATED}


@router.put("/{comment_id}", response_model=CommentResponse)
async def edit_comment(
    body: CommentEditModel,
    user: User = Depends(token_service.get_current_user),
    db: Session = Depends(get_db),
):
    comment = await repository_comments.edit_comment(
        body.comment_id, body.new_text, user, db
    )
    return {"comment": comment, "detail": COMMENT_EDITED}


@router.delete("/{comment_id}", response_model=CommentResponse)
async def delete_comment(
    comment_id: str,
    user: User = Depends(token_service.get_current_user),
    db: Session = Depends(get_db),
):
    comment = await repository_comments.delete_comment(comment_id, user, db)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=COMMENT_DOES_NOT_EXIST
        )
    return {"comment": comment, "detail": COMMENT_DELETED}


@router.get("/{photo_id}", response_model=CommentsResponse)
async def get_comments(photo_id: str, db: Session = Depends(get_db)):
    comments = await repository_comments.get_comments(photo_id, db)
    if not comments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_COMMENTS)
    return {"comments": comments, "detail": COMMENTS_FOUND}
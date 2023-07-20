from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    status,
    UploadFile,
    File,
    Form,
    HTTPException,
    status,
    Query,
)
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import (
    PhotoResponse,
    PhotosResponse,
    PhotoTagModel,
    PhotoFilterModel,
    PhotoHandleModel,
    PhotoEditModel,
)
from src.database.models import Photo, User
from src.repository import photos as repository_photos
from src.services.auth import token_service
from src.messages import *


router = APIRouter(prefix="/photos", tags=["photos"])


@router.post("/", response_model=PhotoResponse, status_code=status.HTTP_201_CREATED)
async def create_photo(
    file: UploadFile = File(),
    description: Optional[str] = Form(None),
    tags: Optional[List[str]] = Form(None),
    user: User = Depends(token_service.get_current_user),
    db: Session = Depends(get_db),
) -> Photo:
    photo = await repository_photos.create_photo(file, description, tags, db, user)
    return {"photo": photo, "detail": PHOTO_POSTED}


@router.delete("/{photo_id}", response_model=PhotoResponse)
async def delete_photo(
    photo_id: str,
    user: User = Depends(token_service.get_current_user),
    db: Session = Depends(get_db),
) -> Photo:
    photo = await repository_photos.delete_photo(photo_id, user, db)
    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=PHOTO_DOES_NOT_EXIST,
        )
    return {"photo": photo, "detail": PHOTO_DELETED}


@router.put("/{photo_id}", response_model=PhotoResponse)
async def edit_description(
    body: PhotoEditModel,
    user: User = Depends(token_service.get_current_user),
    db: Session = Depends(get_db),
):
    photo = await repository_photos.edit_description(body.photo_id, body.description, user, db)
    return {"photo": photo, "detail": PHOTO_DESCRIPTION_EDITED}


@router.get("/", response_model=PhotosResponse)
async def search_photos(
    tag: str = Query(None, description="Tag for searching photos", min_length=1),
    keyword: str = Query(
        None, description="Keyword for searching photos", min_length=1
    ),
    db: Session = Depends(get_db),
):
    photos = await repository_photos.search_photos(tag, keyword, db)
    if photos:
        return {"photos": photos, "detail": PHOTOS_SEARCHED}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=PHOTOS_NOT_FOUND,
    )


@router.get("/{photo_id}", response_model=PhotoResponse)
async def get_photo(photo_id: str, db: Session = Depends(get_db)):
    photo = await repository_photos.get_record(photo_id, Photo, db)
    if photo:
        return {"photo": photo, "detail": PHOTO_FOUND}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=PHOTO_DOES_NOT_EXIST
    )


@router.put("/{photo_id}/tags", response_model=PhotoResponse)
async def add_tags(
    body: PhotoTagModel,
    user: User = Depends(token_service.get_current_user),
    db: Session = Depends(get_db),
):
    photo = await repository_photos.add_tags(body.photo_id, body.tags, user, db)
    if photo:
        return {"photo": photo, "detail": PHOTO_TAG_ADDED}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=PHOTO_DOES_NOT_EXIST
    )


@router.put("/{photo_id}/filter", response_model=PhotoResponse)
async def add_filter(
    body: PhotoFilterModel,
    user: User = Depends(token_service.get_current_user),
    db: Session = Depends(get_db),
):
    photo = await repository_photos.add_filter(body.photo_id, body.filtername, user, db)
    return {"photo": photo, "detail": PHOTO_FILTER_ADDED}


#todo: QR-code
#@router.put("/{photo_id}/transform", response_model=PhotoQrResponse)
async def transform_photo(body: PhotoHandleModel, db: Session = Depends(get_db)):
    photo = await repository_photos.get_record(body.photo_id, Photo, db)
    qrcode = await repository_photos.create_qrcode(photo.url, db)
    return {"photo_id": body.photo_id, "url": photo.url, "qrcode": qrcode}
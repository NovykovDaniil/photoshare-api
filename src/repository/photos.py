from typing import List

from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from PIL import Image
from cloudinary.exceptions import Error as CloudinaryError

from src.database.models import Photo, User, Tag, Comment
from src.schemas import TagModel
from src.repository.tags import create_tag
from src.services.photos import UploadService
from src.services.role import role_service
from src.messages import *


async def inspect_tags(tag_names: List[str], db: Session) -> List[Tag]:
    result = []
    for tag_name in tag_names[0].split(','):
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if tag:
            result.append(tag)
        else:
            tag_model = TagModel(tag=tag_name)
            new_tag = await create_tag(tag_model, db)
            result.append(new_tag)
            db.add(new_tag)
            db.commit()
            db.refresh(new_tag)
    return result


async def get_record(
    record_id: str, table: Photo | Comment, db: Session
) -> Photo | Comment:
    record = db.query(table).filter(table.id == record_id).first()
    return record


async def verify_record(
    record_id: str, table: Photo | Comment, user: User, db: Session
) -> Photo | Comment:
    record = await get_record(record_id, table, db)
    is_moder = await role_service.is_moder(user)
    if record is None or record.user_id != user.id and not is_moder:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=NO_RECORD,
        )
    if record.user_id == user.id or is_moder:
        return record


async def create_photo(
    file: UploadFile,
    description: str | None,
    tags: List[str] | None,
    db: Session,
    user: User,
) -> Photo:
    if file.content_type.split("/")[0] != "image":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ONLY_IMGS,
        )

    public_id = UploadService.create_name(user.email, "RestAPI")
    r = UploadService.upload(file.file, public_id)

    with Image.open(file.file) as img:
        width, height = img.size

    url = UploadService.get_url(public_id, r.get("version"), width=width, height=height)

    new_photo = Photo(
        description=description,
        user_id=user.id,
        filename=file.filename,
        width=width,
        height=height,
        url=url,
    )
    new_photo.tags.clear()
    if tags:
        tags = await inspect_tags(tags, db)
        if len(tags) > 5:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=TOO_MANY_TAGS)
        for tag in tags:
            new_photo.tags.append(tag)

    user.photo_count += 1

    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)

    return new_photo


async def delete_photo(photo_id: str, user: User, db: Session) -> Photo:
    photo = await verify_record(photo_id, Photo, user, db)
    if photo:
        user.photo_count -= 1
        db.delete(photo)
        db.commit()
    return photo


async def edit_description(
    photo_id: str, description: str, user: User, db: Session
) -> Photo:
    photo = await verify_record(photo_id, Photo, user, db)
    photo.description = description
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo


async def search_photos(tag: str, keyword: str, db: Session) -> List[Photo]:
    result = []
    tag = db.query(Tag).filter(Tag.name == tag).first()
    if tag:
        searched_by_tag = [photo for photo in tag.photos]
        result.extend(searched_by_tag)
    if keyword:
        searched_by_keyword = (
            db.query(Photo).filter(Photo.description.like(f"%{keyword}%")).all()
        )
        result.extend(searched_by_keyword)
    return result


async def add_tags(photo_id: str, tags: List[str], user: User, db: Session) -> Photo:
    photo = await verify_record(photo_id, Photo, user, db)
    tags = await inspect_tags(tags, db)

    for tag in tags:
        photo.tags.append(tag)
    if len(photo.tags) > 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=TOO_MANY_TAGS)
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo


async def add_filter(photo_id: str, filtername: str, user: User, db: Session) -> Photo:
    photo = await verify_record(photo_id, Photo, user, db)
    if photo:
        try:
            transformed_image_url = UploadService.add_filter(photo.url, filtername)
        except CloudinaryError as er:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=NO_FILTER)
        photo.url = transformed_image_url
        db.add(photo)
        db.commit()
        db.refresh(photo)
        return photo
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=NO_PHOTO_OR_NOT_YOUR
    )
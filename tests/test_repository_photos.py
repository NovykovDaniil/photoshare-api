from datetime import datetime
from pytest import mark

from src.database.models import User, Photo, Tag
from src.repository.photos import (
    inspect_tags,
    get_record,
    verify_record,
    create_photo,
    delete_photo,
    edit_description,
    search_photos,
    add_tags,
    add_filter,
)


@mark.asyncio
async def test_inspect_tags(db_session):
    tag_names = ["tag1,tag2,tag3"]
    tags = await inspect_tags(tag_names, db_session)

    assert len(tags) == 3
    assert all(isinstance(tag, Tag) for tag in tags)


@mark.asyncio
async def test_get_record_photo(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)

    photo_id = "test_photo_id"
    photo = Photo(user_id=user.id, filename="test.jpg")
    db_session.add(photo)
    db_session.commit()

    result = await get_record(photo_id, Photo, db_session)

    assert isinstance(result, Photo)
    assert result.photo_id == photo_id


@mark.asyncio
async def test_verify_record_photo(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)

    photo_id = "test_photo_id"
    photo = Photo(user_id=user.id, filename="test.jpg")
    db_session.add(photo)
    db_session.commit()

    result = await verify_record(photo_id, Photo, user, db_session)

    assert isinstance(result, Photo)
    assert result.photo_id == photo_id


@mark.asyncio
async def test_create_photo(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    file = "test.jpg"
    description = "Test photo description"
    tags = ["tag1", "tag2"]

    photo = await create_photo(file, description, tags, db_session, user)

    assert photo is not None
    assert photo.description == description
    assert len(photo.tags) == len(tags)
    assert photo.user_id == user.id
    assert isinstance(photo.created_at, datetime)

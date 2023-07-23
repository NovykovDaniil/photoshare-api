from sqlalchemy.orm import Session
from pytest import mark

# Импортируем функции, которые будем тестировать
from photos import (
    inspect_tags,
    create_photo,
    delete_photo,
    edit_description,
    search_photos,
    add_tags,
    add_filter,
)
from src.database.models import Photo, User, Tag
from src.schemas import TagModel
from src.repository.tags import create_tag
from src.messages import ONLY_IMGS, UP_TO_5_TAGS, NO_FILTER, NO_PHOTO, NO_PHOTO_OR_NOT_YOUR


@mark.asyncio
async def test_inspect_tags(db_session):
    """Тест функции inspect_tags."""

    # Создаем тестовые данные
    tag_names = ["tag1,tag2,tag3"]

    # Вызываем тестируемую функцию
    tags = await inspect_tags(tag_names, db_session)

    # Проверяем результаты
    assert isinstance(tags, list)
    assert len(tags) == 3
    assert all(isinstance(tag, Tag) for tag in tags)
    assert all(tag.name in tag_names[0].split(',') for tag in tags)


@mark.asyncio
async def test_create_photo(db_session):
    """Тест функции create_photo."""

    # Создаем тестовые данные
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    file = "test_photo.jpg"
    description = "Test photo"
    tags = ["tag1", "tag2"]

    # Вызываем тестируемую функцию
    photo = await create_photo(file, description, tags, db_session, user)

    # Проверяем результаты
    assert photo is not None
    assert photo.filename == file
    assert photo.description == description
    assert photo.user_id == user.id
    assert photo.tags
    assert len(photo.tags) == 2
    assert all(tag.name in tags for tag in photo.tags)
    assert user.photo_count == 1


@mark.asyncio
async def test_delete_photo(db_session):
    """Тест функции delete_photo."""

    # Создаем тестовые данные
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)

    photo_id = "test_photo_id"
    photo = Photo(id=photo_id, user_id=user.id)
    db_session.add(photo)
    db_session.commit()

    # Вызываем тестируемую функцию
    result = await delete_photo(photo_id, user, db_session)

    # Проверяем результаты
    assert result is not None
    assert result.id == photo_id
    assert db_session.query(Photo).filter(Photo.id == photo_id).first() is None
    assert user.photo_count == 0


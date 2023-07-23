from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from pytest import mark

# Импортируем функции, которые будем тестировать
from comments import (
    create_comment,
    edit_comment,
    delete_comment,
    get_comments,
)
from src.database.models import Photo, User, Comment
from src.repository.photos import get_record, verify_record
from src.messages import NO_PHOTO


@mark.asyncio
async def test_create_comment(db_session):
    """Тест функции create_comment."""

    # Создаем тестовые данные
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    photo_id = "test_photo_id"
    text = "Test comment text"

    # Вызываем тестируемую функцию
    comment = await create_comment(photo_id, text, user, db_session)

    # Проверяем результаты
    assert comment is not None
    assert comment.photo_id == photo_id
    assert comment.user_id == user.id
    assert comment.text == text
    assert isinstance(comment.created_at, datetime)


@mark.asyncio
async def test_edit_comment(db_session):
    """Тест функции edit_comment."""

    # Создаем тестовые данные
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)

    photo_id = "test_photo_id"
    text = "Test comment text"

    comment = Comment(text=text, photo_id=photo_id, user_id=user.id)
    db_session.add(comment)
    db_session.commit()

    new_text = "Updated comment text"

    # Вызываем тестируемую функцию
    updated_comment = await edit_comment(comment.id, new_text, user, db_session)

    # Проверяем результаты
    assert updated_comment is not None
    assert updated_comment.id == comment.id
    assert updated_comment.photo_id == photo_id
    assert updated_comment.user_id == user.id
    assert updated_comment.text == new_text
    assert isinstance(updated_comment.updated_at, datetime)


@mark.asyncio
async def test_delete_comment(db_session):
    """Тест функции delete_comment."""

    # Создаем тестовые данные
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)

    photo_id = "test_photo_id"
    text = "Test comment text"

    comment = Comment(text=text, photo_id=photo_id, user_id=user.id)
    db_session.add(comment)
    db_session.commit()

    # Вызываем тестируемую функцию
    deleted_comment = await delete_comment(comment.id, user, db_session)

    # Проверяем результаты
    assert deleted_comment is not None
    assert deleted_comment.id == comment.id
    assert deleted_comment.photo_id == photo_id
    assert deleted_comment.user_id == user.id

    # Проверяем, что комментарий действительно удален из базы данных
    assert db_session.query(Comment).filter(Comment.id == comment.id).first() is None


@mark.asyncio
async def test_get_comments(db_session):
    """Тест функции get_comments."""

    # Создаем тестовые данные
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)

    photo_id = "test_photo_id"
    text = "Test comment text"

    comment1 = Comment(text=text, photo_id=photo_id, user_id=user.id)
    comment2 = Comment(text=text, photo_id=photo_id, user_id=user.id)
    db_session.add_all([comment1, comment2])
    db_session.commit()

    # Вызываем тестируемую функцию
    comments = await get_comments(photo_id, db_session)

    # Проверяем результаты
    assert isinstance(comments, list)
    assert len(comments) == 2
    assert all(comment.photo_id == photo_id for comment in comments)

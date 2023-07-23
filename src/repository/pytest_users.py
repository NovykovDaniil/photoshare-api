from sqlalchemy.orm import Session
from pytest import mark

# Импортируем функции, которые будем тестировать
from users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar,
    change_password,
    get_user,
    edit_user,
    change_user_active,
)
from src.database.models import User, UserRole
from src.schemas import UserModel
from src.messages import NOT_YOUR_ACCOUNT


@mark.asyncio
async def test_create_user(db_session):
    """Тест функции create_user."""

    # Создаем тестовые данные
    user_model = UserModel(
        email="test@example.com",
        username="testuser",
        password="testpassword",
        full_name="Test User",
    )

    # Вызываем тестируемую функцию
    user = await create_user(user_model, db_session)

    # Проверяем результаты
    assert user is not None
    assert user.email == user_model.email
    assert user.username == user_model.username
    assert user.full_name == user_model.full_name
    assert user.role == UserRole.ADMIN  # Проверяем, что первый созданный пользователь получает роль ADMIN


@mark.asyncio
async def test_update_token(db_session):
    """Тест функции update_token."""

    # Создаем тестовые данные
    user = User(email="test@example.com", username="testuser", password="testpassword")
    db_session.add(user)
    db_session.commit()

    token = "test_token"

    # Вызываем тестируемую функцию
    await update_token(user, token, db_session)

    # Проверяем результаты
    user = await get_user_by_email(user.email, db_session)
    assert user.refresh_token == token


@mark.asyncio
async def test_confirmed_email(db_session):
    """Тест функции confirmed_email."""

    # Создаем тестовые данные
    user = User(email="test@example.com", username="testuser", password="testpassword")
    db_session.add(user)
    db_session.commit()

    # Вызываем тестируемую функцию
    await confirmed_email(user.email, db_session)

    # Проверяем результаты
    user = await get_user_by_email(user.email, db_session)
    assert user.confirmed is True

from datetime import datetime
from typing import List

from pydantic import EmailStr, Field

from src.database.models import UserRole
from src.services import schemas

def test_user_model():
    user_model = schemas.UserModel(
        username="testuser",
        email="testuser@example.com",
        password="password123",
    )
    assert user_model.username == "testuser"
    assert user_model.email == "testuser@example.com"
    assert user_model.password == "password123"

def test_user_db():
    user_db = schemas.UserDb(
        id="1",
        username="testuser",
        bio="Test bio",
        email="testuser@example.com",
        role=UserRole.USER,
        created_at=datetime.utcnow(),
        avatar="test.jpg",
        photo_count=10,
        subscriptions=5,
        subscribers=8,
        confirmed=True,
        is_active=True,
    )
    assert user_db.id == "1"
    assert user_db.username == "testuser"
    assert user_db.bio == "Test bio"
    assert user_db.email == "testuser@example.com"
    assert user_db.role == UserRole.USER
    assert isinstance(user_db.created_at, datetime)
    assert user_db.avatar == "test.jpg"
    assert user_db.photo_count == 10
    assert user_db.subscriptions == 5
    assert user_db.subscribers == 8
    assert user_db.confirmed == True
    assert user_db.is_active == True

def test_user_response():
    user_db = schemas.UserDb(
        id="1",
        username="testuser",
        bio="Test bio",
        email="testuser@example.com",
        role=UserRole.USER,
        created_at=datetime.utcnow(),
        avatar="test.jpg",
        photo_count=10,
        subscriptions=5,
        subscribers=8,
        confirmed=True,
        is_active=True,
    )
    user_response = schemas.UserResponse(
        user=user_db,
        detail="User successfully created",
    )
    assert user_response.user == user_db
    assert user_response.detail == "User successfully created"

def test_user_reset_password():
    user_reset_password = schemas.UserResetPassword(
        email="testuser@example.com",
        reset_code=123456,
        new_password="newpassword123",
    )
    assert user_reset_password.email == "testuser@example.com"
    assert user_reset_password.reset_code == 123456
    assert user_reset_password.new_password == "newpassword123"

# Тесты для других схем данных могут быть написаны по аналогии с предыдущими.
# ... (дополнительные тесты для остальных схем данных)

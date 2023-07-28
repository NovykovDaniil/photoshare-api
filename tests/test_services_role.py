import pytest
from unittest.mock import AsyncMock, MagicMock

from src.services.role import Role
from src.database.models import User

@pytest.fixture
def role_service():
    return Role()

@pytest.fixture
def admin_user():
    user = User(role="admin")
    return user

@pytest.fixture
def moder_user():
    user = User(role="moderator")
    return user

def test_is_admin(role_service, admin_user):
    assert role_service.is_admin(admin_user) == True

def test_is_not_admin(role_service, moder_user):
    assert role_service.is_admin(moder_user) == False

def test_is_moder(role_service, moder_user):
    assert role_service.is_moder(moder_user) == True

def test_is_not_moder(role_service, admin_user):
    assert role_service.is_moder(admin_user) == False

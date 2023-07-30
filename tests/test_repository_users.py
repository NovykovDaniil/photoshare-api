import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.database.models import User
from src.repository.users import get_user_by_email, update_token, confirmed_email, update_avatar, change_password, get_user


class TestUserRepository(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.session_mock = MagicMock(spec=Session)
        self.user_mock = MagicMock(spec=User)

    async def test_get_user_by_email(self):
        self.user_mock.email = "test_email"
        self.session_mock.query().filter().first.return_value = self.user_mock
        result = await get_user_by_email("test_email", self.session_mock)
        self.assertEqual(result, self.user_mock)

    async def test_update_token(self):
        token = "new_token"
        self.session_mock.query().filter().first.return_value = self.user_mock
        await update_token(self.user_mock, token, self.session_mock)
        self.assertEqual(self.user_mock.refresh_token, token)

    async def test_confirmed_email(self):
        self.session_mock.query().filter().first.return_value = self.user_mock
        await confirmed_email("test_email", self.session_mock)
        self.assertEqual(self.user_mock.confirmed, True)

    async def test_update_avatar(self):
        self.session_mock.query().filter().first.return_value = self.user_mock
        await update_avatar("test_email", "new_avatar_url", self.session_mock)
        self.assertEqual(self.user_mock.avatar, "new_avatar_url")

    async def test_change_password(self):
        self.session_mock.query().filter().first.return_value = self.user_mock
        await change_password(self.user_mock, "new_password", self.session_mock)
        self.assertEqual(self.user_mock.password, "new_password")

    async def test_get_user(self):
        self.user_mock.username = "test_username"
        self.session_mock.query().filter().first.return_value = self.user_mock
        result = await get_user("test_username", self.session_mock)
        self.assertEqual(result, self.user_mock)


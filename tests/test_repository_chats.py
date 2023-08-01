from unittest.mock import patch, MagicMock
import unittest
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.repository import chats
from src.database.models import User, Chat, Message
import pytest

user = User(id=1, username="test", email="test@test.com")
chat = Chat(id=1, interlocutor_1=1, interlocutor_2=2)


class TestChats(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.session = MagicMock(spec=Session)
        self.interlocutor_id = 'interlocutor_id'
        self.user = User(id='user_id')

    async def test_create_chat_user_not_found(self):
        self.session.query().filter().first.return_value = None
        with self.assertRaises(HTTPException) as context:
            await chats.create_chat(self.interlocutor_id, self.user, self.session)
        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(context.exception.detail, 'There are no user with such id')

    async def test_delete_chat(self):
        session_mock = MagicMock()
        session_mock.query().filter().first.return_value = chat
        with patch('src.repository.chats.role_service.is_admin', return_value=False):
            result = await chats.delete_chat(1, user, session_mock)
            self.assertIsNotNone(result)


    async def test_get_chat(self):
        session_mock = MagicMock()
        session_mock.query().filter().first.return_value = chat
        with patch('src.repository.chats.role_service.is_admin', return_value=False):
            result = await chats.get_chat(1, user, session_mock)
            self.assertEqual(result, chat) 


    async def test_get_messages(self):
        chat_with_message = Chat(id=1, interlocutor_1=1, interlocutor_2=2, messages=[Message(id=1, sender=1, recipient=2, text='test_text')])
        session_mock = MagicMock()
        with patch('src.repository.chats.get_chat', return_value=chat_with_message):
            result = await chats.get_messages(1, user, session_mock)
            self.assertEqual(result, chat_with_message.messages)

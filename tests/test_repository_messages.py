import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import HTTPException
from src.database.models import User, Message, Chat
from sqlalchemy.orm import Session
from src.repository import messages as repository_messages
from main import app


user = User(id=1)  
chat = Chat(id='chat_id', interlocutor_1=user.id, interlocutor_2=2)  
message = Message(id='message_id', sender=user.id, text='original_text')  


class TestMessages(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def setUp(self):
        self.user_mock = User(id="123", username='test_user')
        self.mock_session = MagicMock(spec=Session)

    @patch('src.database.db.get_db')
    async def test_create_message(self, mock_get_db):
        mock_get_db.return_value = self.mock_session
        self.mock_session.query(Chat).filter().first.return_value = None
        with self.assertRaises(HTTPException):
            await repository_messages.create_message("chat_id", "text", self.user_mock, self.mock_session)

    @patch('src.database.db.get_db')
    async def test_get_message(self, mock_get_db):
        mock_get_db.return_value = self.mock_session
        self.mock_session.query(Message).filter().first.return_value = None
        with self.assertRaises(HTTPException):
            await repository_messages.get_message("message_id", self.user_mock, self.mock_session)

    @patch('src.database.db.get_db')
    @patch('src.repository.messages.get_message')
    async def test_edit_message(self, mock_get_message, mock_get_db):
        mock_get_db.return_value = self.mock_session
        mock_get_message.return_value = Message(id="message_id", text="old_text")
        edited_message = await repository_messages.edit_message("message_id", "new_text", self.user_mock, self.mock_session)
        self.assertEqual(edited_message.text, "new_text")

    @patch('src.database.db.get_db')
    @patch('src.repository.messages.get_message')
    async def test_delete_message(self, mock_get_message, mock_get_db):
        mock_get_db.return_value = self.mock_session
        mock_get_message.return_value = Message(id="message_id", text="old_text")
        deleted_message = await repository_messages.delete_message("message_id", self.user_mock, self.mock_session)
        self.assertEqual(deleted_message.id, "message_id")


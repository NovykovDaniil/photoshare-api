from fastapi.testclient import TestClient
from unittest import TestCase
from unittest.mock import AsyncMock, patch
from main import app  
from src.database.models import User, Chat, Message

client = TestClient(app)

class TestChatsRoutes(TestCase):
    def setUp(self):
        self.test_user = User(id="test_id", username="test_username", password="test_password")
        self.test_chat = Chat(id="test_chat_id", interlocutor_1=self.test_user.id, interlocutor_2="other_user_id")

    @patch("src.repository.chats.create_chat")
    def test_create_chat(self, mock_create_chat):
        mock_create_chat.return_value = AsyncMock(return_value=self.test_chat)

        response = client.post("/chats/", json={"interlocutor_id": "other_user_id"}, headers={"Authorization": f"Bearer {self.test_user.id}"})

        self.assertEqual(response.status_code, 404)

    @patch("src.repository.chats.delete_chat")
    def test_delete_chat(self, mock_delete_chat):
        mock_delete_chat.return_value = AsyncMock(return_value=self.test_chat)

        response = client.delete(f"/chats/{self.test_chat.id}", headers={"Authorization": f"Bearer {self.test_user.id}"})

        self.assertEqual(response.status_code, 404)

    @patch("src.repository.chats.get_chat")
    def test_get_chat(self, mock_get_chat):
        mock_get_chat.return_value = AsyncMock(return_value=self.test_chat)

        response = client.get(f"/chats/{self.test_chat.id}", headers={"Authorization": f"Bearer {self.test_user.id}"})

        self.assertEqual(response.status_code, 404)

    @patch("src.repository.chats.get_messages")
    def test_get_messages(self, mock_get_messages):
        test_messages = [Message(id="message_id", sender=self.test_user.id, recipient="other_user_id", text="Test message.")]
        mock_get_messages.return_value = AsyncMock(return_value=test_messages)

        response = client.get(f"/chats/{self.test_chat.id}/messages", headers={"Authorization": f"Bearer {self.test_user.id}"})

        self.assertEqual(response.status_code, 404)

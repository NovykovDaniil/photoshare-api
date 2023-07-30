from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
from src.database.models import Message

client = TestClient(app)

def test_create_message():
    with patch('src.repository.messages.create_message') as mock:
        mock.return_value = Message(id='1', sender=1, recipient=2, text='test_text')
        response = client.post('/api/messages/', json={'chat_id': '1', 'text': 'test_text'})
        assert response.status_code == 401

def test_edit_message():
    with patch('src.repository.messages.edit_message') as mock:
        mock.return_value = Message(id='1', sender=1, recipient=2, text='edited_text')
        response = client.put('/api/messages/1', json={'message_id': '1', 'text': 'edited_text'})
        assert response.status_code == 401

def test_delete_message():
    with patch('src.repository.messages.delete_message') as mock:
        mock.return_value = Message(id='1', sender=1, recipient=2, text='test_text')
        response = client.delete('/api/messages/1')
        assert response.status_code == 401

def test_get_message():
    with patch('src.repository.messages.get_message') as mock:
        mock.return_value = Message(id='1', sender=1, recipient=2, text='test_text')
        response = client.get('/api/messages/1')
        assert response.status_code == 401

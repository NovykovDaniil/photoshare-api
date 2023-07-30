from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, ANY
from src.database.models import User
from src.database.db import get_db
from fastapi import status


def override_get_db():
    yield {}


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_get_user():
    with patch('src.repository.users.get_user') as mock:
        mock.return_value = User(username='test_user', bio='test_bio')
        response = client.get('/users/test_user')
        assert response.status_code == 404
        

def test_get_user_not_found():
    with patch('src.repository.users.get_user', return_value=None) as mock:
        response = client.get('/users/non_existent_user')
        assert response.status_code == status.HTTP_404_NOT_FOUND


def test_edit_user():
    with patch('src.repository.users.edit_user') as mock:
        mock.return_value = User(username='test_user', bio='new_bio')
        response = client.put('/users/test_user/edit', json={'username': 'test_user', 'bio': 'new_bio'})
        assert response.status_code == 404


def test_edit_user_not_found():
    with patch('src.repository.users.edit_user', return_value=None) as mock:
        response = client.put('/users/non_existent_user/edit', json={'username': 'non_existent_user', 'bio': 'new_bio'})
        assert response.status_code == status.HTTP_404_NOT_FOUND


def test_ban_user():
    with patch('src.repository.users.change_user_active') as mock:
        mock.return_value = User(username='test_user', bio='test_bio', is_active=False)
        response = client.put('/users/test_user/active', json={'username': 'test_user'})
        assert response.status_code == 404

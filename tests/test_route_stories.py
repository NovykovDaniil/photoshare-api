import pytest
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.orm import Session
from unittest.mock import MagicMock, patch
from unittest import IsolatedAsyncioTestCase
from src.database.models import User
from src.repository import stories as repository_stories
from src.services.auth import token_service
from src.schemas import StoryResponse, StoriesResponse
from src.database.db import get_db
from src.constants import NO_STORY, STORY_CREATED, STORY_DELETED, STORY_FOUND, NOT_FOUND
from main import app

class TestStories(IsolatedAsyncioTestCase):

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = TestClient(app)
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.file = MagicMock()

    @patch('src.repository.stories.create_story')
    def test_create_story_success(self, mock_create_story):
        mock_create_story.return_value = {'id': 'story_id', 'name': self.file.filename}
        response = self.client.post(
            '/stories/',
            headers={'Authorization': 'Bearer dummy_token'},
            files={'file': self.file},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('src.repository.stories.create_story')
    def test_create_story_failed(self, mock_create_story):
        mock_create_story.side_effect = Exception("Error occurred")
        response = self.client.post(
            '/stories/',
            headers={'Authorization': 'Bearer dummy_token'},
            files={'file': self.file},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('src.repository.stories.delete_story')
    def test_delete_story_success(self, mock_delete_story):
        mock_delete_story.return_value = {'id': 'existing_story_id', 'name': 'test.jpg'}
        response = self.client.delete(
            '/stories/existing_story_id',
            headers={'Authorization': 'Bearer dummy_token'},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('src.repository.stories.delete_story')
    def test_delete_story_not_found(self, mock_delete_story):
        mock_delete_story.return_value = None
        response = self.client.delete(
            '/stories/nonexistent_story_id',
            headers={'Authorization': 'Bearer dummy_token'},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('src.repository.stories.get_story')
    def test_get_story_success(self, mock_get_story):
        mock_get_story.return_value = {'id': 'existing_story_id', 'name': 'test.jpg'}
        response = self.client.get('/stories/existing_story_id')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('src.repository.stories.get_story')
    def test_get_story_not_found(self, mock_get_story):
        mock_get_story.return_value = None
        response = self.client.get('/stories/nonexistent_story_id')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {'detail': NOT_FOUND}

    @patch('src.repository.stories.recommend')
    def test_recommend_not_found(self, mock_recommend):
        mock_recommend.return_value = None
        response = self.client.get('/stories/', headers={'Authorization': 'Bearer dummy_token'})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {'detail': NOT_FOUND}
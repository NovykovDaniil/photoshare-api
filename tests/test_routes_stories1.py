from fastapi import status, UploadFile
from sqlalchemy.orm import Session

from src.database.models import User
from src.services import stories
from src.repository import stories as repository_stories
from src.messages import STORY_CREATED, STORY_DELETED, NO_STORY, STORY_FOUND, NO_STORIES, STORIES_FOUND

class MockUploadFile(UploadFile):
    def __init__(self, filename: str):
        self.filename = filename

class MockStory:
    def __init__(self, id: str, url: str, user_id: str):
        self.id = id
        self.url = url
        self.user_id = user_id

def test_create_story(monkeypatch):
    def mock_create_story(file: UploadFile, user: User, db: Session):
        return MockStory(id="1", url="test.jpg", user_id="1")
    
    monkeypatch.setattr(repository_stories, "create_story", mock_create_story)
    router = stories.router
    response = router.post('/stories/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'story': {'id': '1', 'url': 'test.jpg', 'user_id': '1'}, 'detail': STORY_CREATED}

def test_delete_story(monkeypatch):
    def mock_delete_story(story_id: str, user: User, db: Session):
        return MockStory(id="1", url="test.jpg", user_id="1")
    
    monkeypatch.setattr(repository_stories, "delete_story", mock_delete_story)
    router = stories.router
    response = router.delete('/stories/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'story': {'id': '1', 'url': 'test.jpg', 'user_id': '1'}, 'detail': STORY_DELETED}

def test_get_story(monkeypatch):
    def mock_get_story(story_id: str, db: Session):
        return MockStory(id="1", url="test.jpg", user_id="1")
    
    monkeypatch.setattr(repository_stories, "get_story", mock_get_story)
    router = stories.router
    response = router.get('/stories/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'story': {'id': '1', 'url': 'test.jpg', 'user_id': '1'}, 'detail': STORY_FOUND}

def test_recommend(monkeypatch):
    def mock_recommend(user: User, db: Session):
        return [MockStory(id="1", url="test.jpg", user_id="1"), MockStory(id="2", url="test2.jpg", user_id="2")]
    
    monkeypatch.setattr(repository_stories, "recommend", mock_recommend)
    router = stories.router
    response = router.get('/stories/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'stories': [
            {'id': '1', 'url': 'test.jpg', 'user_id': '1'},
            {'id': '2', 'url': 'test2.jpg', 'user_id': '2'}
        ],
        'detail': STORIES_FOUND
    }

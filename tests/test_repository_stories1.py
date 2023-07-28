from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.database.models import User, Story, Subscription
from src.repository import stories as repository_stories
from src.services.photos import UploadService
from src.services.role import Role
import pytest

class FakeUploadFile:
    def __init__(self, content_type="video/mp4"):
        self.content_type = content_type
        self.file = b"fake_file_content"

def test_verify_story():
    user = User(id="1", username="testuser", email="testuser@example.com")
    story = Story(id="1", url="fake_story_url", user_id="1", created_at=datetime.utcnow(), expire_to=datetime.utcnow() + timedelta(days=1))

    assert repository_stories.verify_story(story, user) == True

    user.id = "2"
    assert repository_stories.verify_story(story, user) == False

    user.role = Role()
    assert repository_stories.verify_story(story, user) == True

def test_get_story(db_session):
    story = Story(id="1", url="fake_story_url", user_id="1", created_at=datetime.utcnow(), expire_to=datetime.utcnow() + timedelta(days=1))
    db_session.add(story)
    db_session.commit()

    assert repository_stories.get_story("1", db_session) == story

    with pytest.raises(HTTPException) as e:
        repository_stories.get_story("2", db_session)
    assert e.value.status_code == status.HTTP_400_BAD_REQUEST
    assert e.value.detail == "Story is already inaccessible"

def test_create_story(monkeypatch, db_session):
    async def fake_upload_video(file, public_id):
        return {"version": "fake_version"}

    monkeypatch.setattr(UploadService, "upload_video", fake_upload_video)

    user = User(id="1", username="testuser", email="testuser@example.com")
    file = FakeUploadFile()

    story = repository_stories.create_story(file, user, db_session)
    assert story.url == "fake_story_url"
    assert story.user_id == "1"
    assert story.created_at <= datetime.utcnow()
    assert story.expire_to > datetime.utcnow()

def test_create_story_invalid_file(monkeypatch, db_session):
    user = User(id="1", username="testuser", email="testuser@example.com")
    file = FakeUploadFile(content_type="image/jpeg")

    with pytest.raises(HTTPException) as e:
        repository_stories.create_story(file, user, db_session)
    assert e.value.status_code == status.HTTP_400_BAD_REQUEST
    assert e.value.detail == "You can upload only videos"

def test_delete_story(db_session):
    user = User(id="1", username="testuser", email="testuser@example.com")
    story = Story(id="1", url="fake_story_url", user_id="1", created_at=datetime.utcnow(), expire_to=datetime.utcnow() + timedelta(days=1))
    db_session.add(story)
    db_session.commit()

    assert repository_stories.delete_story("1", user, db_session) == story
    assert db_session.query(Story).filter(Story.id == "1").count() == 0

    user.id = "2"
    with pytest.raises(HTTPException) as e:
        repository_stories.delete_story("1", user, db_session)
    assert e.value.status_code == status.HTTP_403_FORBIDDEN
    assert e.value.detail == "Story is already inaccessible"

def test_recommend(db_session):
    user = User(id="1", username="testuser", email="testuser@example.com")
    db_session.add(user)

    author1 = User(id="2", username="author1", email="author1@example.com")
    db_session.add(author1)

    author2 = User(id="3", username="author2", email="author2@example.com")
    db_session.add(author2)

    db_session.commit()

    db_session.add(Subscription(subscriber_id="1", author_id="2"))
    db_session.add(Subscription(subscriber_id="1", author_id="3"))
    db_session.commit()

    stories = repository_stories.recommend(user, db_session)
    assert len(stories) == 0

    db_session.add(Story(id="1", url="fake_story_url_1", user_id="2", created_at=datetime.utcnow(), expire_to=datetime.utcnow() + timedelta(days=1)))
    db_session.add(Story(id="2", url="fake_story_url_2", user_id="3", created_at=datetime.utcnow(), expire_to=datetime.utcnow() + timedelta(days=1)))
    db_session.commit()

    stories = repository_stories.recommend(user, db_session)
    assert len(stories) == 2

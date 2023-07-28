from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.database.models import User, Story, Subscription
from src.repository import stories
from src.services.photos import UploadService
from src.messages import *
from unittest.mock import MagicMock
import pytest

class FakeUploadService(UploadService):
    @staticmethod
    def create_name(email: str, prefix: str):
        return "fake_public_id"

    @staticmethod
    def upload_video(file, public_id):
        return {"version": "fake_version"}

    @staticmethod
    def get_video_url(public_id, version):
        return "fake_video_url"

def test_verify_story():
    user = User(id="1", username="testuser", email="testuser@example.com")
    story1 = Story(id="1", url="fake_story_url_1", user_id="1", created_at=datetime.utcnow(), expire_to=datetime.utcnow() + timedelta(days=1))
    story2 = Story(id="2", url="fake_story_url_2", user_id="2", created_at=datetime.utcnow(), expire_to=datetime.utcnow() + timedelta(days=1))

    assert stories.verify_story(story1, user) == True
    assert stories.verify_story(story2, user) == False

def test_get_story(db_session):
    story = Story(id="1", url="fake_story_url", user_id="1", created_at=datetime.utcnow(), expire_to=datetime.utcnow() + timedelta(days=1))
    db_session.add(story)
    db_session.commit()

    assert stories.get_story("1", db_session) == story
    with pytest.raises(Exception) as e:
        stories.get_story("2", db_session)
    assert "There is no story with such ID or it is not your story" in str(e.value)

def test_create_story(db_session, monkeypatch):
    monkeypatch.setattr(stories, "UploadService", FakeUploadService)

    user = User(id="1", username="testuser", email="testuser@example.com")

    story = stories.create_story(FakeUploadService(), user, db_session)
    assert story.id == "fake_public_id"
    assert story.url == "fake_video_url"
    assert story.user_id == "1"
    assert "created_at" in story
    assert "expire_to" in story

def test_delete_story(db_session):
    user = User(id="1", username="testuser", email="testuser@example.com")
    story1 = Story(id="1", url="fake_story_url_1", user_id="1", created_at=datetime.utcnow(), expire_to=datetime.utcnow() + timedelta(days=1))
    story2 = Story(id="2", url="fake_story_url_2", user_id="2", created_at=datetime.utcnow(), expire_to=datetime.utcnow() + timedelta(days=1))

    db_session.add(story1)
    db_session.add(story2)
    db_session.commit()

    assert stories.delete_story("1", user, db_session) == story1
    assert stories.delete_story("2", user, db_session) == None

def test_recommend(db_session):
    user1 = User(id="1", username="testuser1", email="testuser1@example.com")
    user2 = User(id="2", username="testuser2", email="testuser2@example.com")
    user3 = User(id="3", username="testuser3", email="testuser3@example.com")

    story1 = Story(id="1", url="fake_story_url_1", user_id="1", created_at=datetime.utcnow(), expire_to=datetime.utcnow() + timedelta(days=1))
    story2 = Story(id="2", url="fake_story_url_2", user_id="2", created_at=datetime.utcnow(), expire_to=datetime.utcnow() + timedelta(days=1))
    story3 = Story(id="3", url="fake_story_url_3", user_id="3", created_at=datetime.utcnow(), expire_to=datetime.utcnow() + timedelta(days=1))

    db_session.add(user1)
    db_session.add(user2)
    db_session.add(user3)
    db_session.add(story1)
    db_session.add(story2)
    db_session.add(story3)
    db_session.add(Subscription(subscriber_id="1", author_id="2"))
    db_session.add(Subscription(subscriber_id="1", author_id="3"))
    db_session.add(Subscription(subscriber_id="2", author_id="3"))
    db_session.commit()

    assert stories.recommend(user1, db_session) == [story2, story3]

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest

from src.database.db import engine, get_db
from src.database.models import Base, User, UserRole
from src.services import token_service
from main import app
from src.schemas import StoryResponse, StoriesResponse


def override_get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

def get_test_user(db: Session):
    user = User(
        username="testuser",
        email="testuser@example.com",
        password="password123",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_test_token(user_id: str):
    access_token = token_service.create_access_token({"sub": user_id})
    return f"Bearer {access_token}"

@pytest.fixture(scope="module")
def test_client():
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.pop(get_db)

def test_create_story(test_client, test_user):
    token = get_test_token(test_user.id)
    with open("test_video.mp4", "rb") as file:
        response = test_client.post(
            "/stories/",
            headers={"Authorization": token},
            files={"file": ("test_video.mp4", file, "video/mp4")},
        )
        assert response.status_code == 200
        data = response.json()
        assert "story" in data
        assert "detail" in data
        assert data["detail"] == "Story successfully created"

def test_get_story(test_client, test_user):
    token = get_test_token(test_user.id)
    with open("test_video.mp4", "rb") as file:
        response = test_client.post(
            "/stories/",
            headers={"Authorization": token},
            files={"file": ("test_video.mp4", file, "video/mp4")},
        )
        assert response.status_code == 200
        data = response.json()
        assert "story" in data
        assert "detail" in data
        story_id = data["story"]["id"]

        response = test_client.get(f"/stories/{story_id}")
        assert response.status_code == 200
        data = response.json()
        assert "story" in data
        assert "detail" in data
        assert data["detail"] == "Story was successfully found"

def test_recommend(test_client, test_user):
    token = get_test_token(test_user.id)
    with open("test_video.mp4", "rb") as file:
        response = test_client.post(
            "/stories/",
            headers={"Authorization": token},
            files={"file": ("test_video.mp4", file, "video/mp4")},
        )
        assert response.status_code == 200

        response = test_client.get("/stories/", headers={"Authorization": token})
        assert response.status_code == 200
        data = response.json()
        assert "stories" in data
        assert "detail" in data
        assert data["detail"] == "Stories was successfully found"

def test_delete_story(test_client, test_user):
    token = get_test_token(test_user.id)
    with open("test_video.mp4", "rb") as file:
        response = test_client.post(
            "/stories/",
            headers={"Authorization": token},
            files={"file": ("test_video.mp4", file, "video/mp4")},
        )
        assert response.status_code == 200
        data = response.json()
        assert "story" in data
        assert "detail" in data
        story_id = data["story"]["id"]

        response = test_client.delete(f"/stories/{story_id}", headers={"Authorization": token})
        assert response.status_code == 200
        data = response.json()
        assert "story" in data
        assert "detail" in data
        assert data["detail"] == "Story was successfully deleted"

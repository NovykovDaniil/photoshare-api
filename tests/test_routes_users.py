from fastapi.testclient import TestClient
from pytest import fixture
from src.database.models import User
from src.repository.users import get_user, edit_user, change_user_active
from src.schemas import UserResponse, UserEditModel, UserBanModel
from main import app

client = TestClient(app)


@fixture(scope="function")
def db_session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


def test_get_user(db_session):
    username = "test_user"
    user = User(username=username, email="test@example.com")
    db_session.add(user)
    db_session.commit()

    response = client.get(f"/users/{username}")

    assert response.status_code == 200
    assert "user" in response.json()
    assert response.json()["user"]["username"] == username
    assert "detail" in response.json()


def test_get_nonexistent_user(db_session):
    response = client.get("/users/nonexistent")

    assert response.status_code == 404
    assert "detail" in response.json()
    assert response.json()["detail"] == "User not found"


def test_edit_user(db_session):
    username = "edit_user"
    bio = "This is an edited user."

    user = User(username=username, email="edit@example.com")
    db_session.add(user)
    db_session.commit()

    response = client.put(
        f"/users/{username}/edit",
        json={"bio": bio},
    )

    assert response.status_code == 200
    assert "user" in response.json()
    assert response.json()["user"]["username"] == username
    assert response.json()["user"]["bio"] == bio
    assert "detail" in response.json()


def test_edit_nonexistent_user(db_session):
    response = client.put(
        "/users/nonexistent/edit",
        json={"bio": "This user does not exist."},
    )

    assert response.status_code == 404
    assert "detail" in response.json()
    assert response.json()["detail"] == "User not found"


def test_change_user_active(db_session):
    username = "test_user"
    user = User(username=username, email="test@example.com", is_active=True)
    db_session.add(user)
    db_session.commit()

    response = client.put(
        f"/users/{username}/active",
        json={"is_active": False},
    )

    assert response.status_code == 200
    assert "user" in response.json()
    assert response.json()["user"]["username"] == username
    assert response.json()["user"]["is_active"] is False
    assert "detail" in response.json()


def test_change_nonexistent_user_active(db_session):
    response = client.put(
        "/users/nonexistent/active",
        json={"is_active": False},
    )

    assert response.status_code == 404
    assert "detail" in response.json()
    assert response.json()["detail"] == "User not found"

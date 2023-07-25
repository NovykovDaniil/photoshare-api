import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.database.models import Base, User

TEST_DATABASE_URL = "sqlite:///./test_db.sqlite3"

@pytest.fixture(scope="module")
def db():
    engine = create_engine(TEST_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()


@pytest.fixture
def client(db):
    def get_test_db():
        return db

    app.dependency_overrides[app.dependencies.get_db] = get_test_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


def test_signup(client):
    response = client.post(
        "/auth/signup",
        json={
            "username": "test_user",
            "email": "test@example.com",
            "password": "test_password",
        },
    )
    assert response.status_code == 201
    assert "user" in response.json()
    assert "detail" in response.json()


def test_signup_conflict(client, db):
    user = User(
        username="existing_user",
        email="test@example.com",
        password="existing_password",
    )
    db.add(user)
    db.commit()

    response = client.post(
        "/auth/signup",
        json={
            "username": "test_user",
            "email": "test@example.com",
            "password": "test_password",
        },
    )
    assert response.status_code == 409
    assert "detail" in response.json()


def test_login(client, db):
    user = User(
        username="test_user",
        email="test@example.com",
        password="test_password",
        confirmed=True,
    )
    db.add(user)
    db.commit()

    response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "test_password"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert "token_type" in response.json()


def test_login_unconfirmed(client, db):
    user = User(
        username="unconfirmed_user",
        email="unconfirmed@example.com",
        password="test_password",
        confirmed=False,
    )
    db.add(user)
    db.commit()

    response = client.post(
        "/auth/login",
        data={"username": "unconfirmed@example.com", "password": "test_password"},
    )
    assert response.status_code == 401
    assert "detail" in response.json()


def test_login_banned(client, db):
    user = User(
        username="banned_user",
        email="banned@example.com",
        password="test_password",
        confirmed=True,
        is_active=False,
    )
    db.add(user)
    db.commit()

    response = client.post(
        "/auth/login",
        data={"username": "banned@example.com", "password": "test_password"},
    )
    assert response.status_code == 401
    assert "detail" in response.json()

def test_logout(client, db):
    user = User(
        username="test_user",
        email="test@example.com",
        password="test_password",
        confirmed=True,
    )
    db.add(user)
    db.commit()

    access_token = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "test_password"},
    ).json()["access_token"]

    response = client.post("/auth/logout", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Logged out successfully"


def test_refresh_token(client, db):
    user = User(
        username="test_user",
        email="test@example.com",
        password="test_password",
        confirmed=True,
    )
    db.add(user)
    db.commit()

    refresh_token = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "test_password"},
    ).json()["refresh_token"]

    response = client.get("/auth/refresh_token", headers={"Authorization": f"Bearer {refresh_token}"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert "token_type" in response.json()


def test_confirmed_email(client, db):
    user = User(
        username="test_user",
        email="test@example.com",
        password="test_password",
        confirmed=False,
    )
    db.add(user)
    db.commit()

    email_confirmation_token = token_service.create_email_confirmation_token(user.email)
    
    response = client.get(f"/auth/confirmed_email/{email_confirmation_token}")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Email confirmed successfully"


def test_request_email(client, db):
    user = User(
        username="test_user",
        email="test@example.com",
        password="test_password",
        confirmed=False,
    )
    db.add(user)
    db.commit()

    access_token = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "test_password"},
    ).json()["access_token"]

    response = client.post(
        "/auth/request_email",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"email": "test@example.com"},
    )
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Check your email for confirmation"


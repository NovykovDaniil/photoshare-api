from fastapi.testclient import TestClient
from jose import jwt
from pytest import fixture
from src.database.models import User
from src.repository.users import create_user
from src.schemas import UserModel
from main import app

client = TestClient(app)


@fixture(scope="function")
def db_session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


def test_create_access_token(db_session):
    user_data = {
        "username": "test_user",
        "email": "test@example.com",
        "password": "test_password",
    }
    user = create_user(UserModel(**user_data), db_session)

    access_token = jwt.encode(
        {"sub": user.email, "scope": "access_token"},
        settings.secret_key,
        algorithm=settings.algorithm,
    )

    response = client.post("/api/auth/login", data={"username": user_data["email"], "password": user_data["password"]})

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["access_token"] == access_token
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_create_refresh_token(db_session):
    user_data = {
        "username": "test_user",
        "email": "test@example.com",
        "password": "test_password",
    }
    user = create_user(UserModel(**user_data), db_session)

    refresh_token = jwt.encode(
        {"sub": user.email, "scope": "refresh_token"},
        settings.secret_key,
        algorithm=settings.algorithm,
    )

    response = client.post("/api/auth/login", data={"username": user_data["email"], "password": user_data["password"]})

    assert response.status_code == 200
    assert "refresh_token" in response.json()
    assert response.json()["refresh_token"] == refresh_token
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_create_email_token():
    user_data = {
        "username": "test_user",
        "email": "test@example.com",
        "password": "test_password",
    }

    email_token = jwt.encode(
        {"sub": user_data["email"]},
        settings.secret_key,
        algorithm=settings.algorithm,
    )

    token = token_service.create_email_token({"sub": user_data["email"]})

    assert token == email_token

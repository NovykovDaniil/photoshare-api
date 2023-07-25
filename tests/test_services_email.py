from fastapi.testclient import TestClient
from pytest import fixture
from src.services.email import send_email_confirmation, send_email_reset
from main import app

client = TestClient(app)


@fixture(scope="function")
def db_session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


def test_send_email_confirmation():
    email = "test@example.com"
    username = "test_user"
    host = "example.com"

    response = send_email_confirmation(email, username, host)

    assert response is None


def test_send_email_reset():
    email = "test@example.com"
    reset_code = "test_reset_code"

    response = send_email_reset(email, reset_code)

    assert response is None

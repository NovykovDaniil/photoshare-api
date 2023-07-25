from fastapi.testclient import TestClient
from pytest import fixture
from src.database.models import User, Subscription
from src.repository.subscriptions import get_subscriptions, subscribe, unsubscribe
from src.schemas import SubscriptionResponse, SubscriptionsResponse
from src.services.auth import token_service
from main import app

client = TestClient(app)


@fixture(scope="function")
def db_session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


def test_get_subscriptions(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    subscription_id = "test_subscription_id"
    subscription = Subscription(id=subscription_id, author_id=2, subscriber_id=user.id)
    db_session.add(subscription)
    db_session.commit()

    response = client.get(
        "/subscriptions/",
        headers={"Authorization": f"Bearer {token_service.create_access_token(data={'sub': user.email})}"}
    )

    assert response.status_code == 200
    assert "subscriptions" in response.json()
    assert len(response.json()["subscriptions"]) == 1
    assert response.json()["subscriptions"][0]["id"] == subscription_id
    assert "detail" in response.json()


def test_subscribe(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    author_id = "test_author_id"

    response = client.post(
        f"/subscriptions/{author_id}",
        headers={"Authorization": f"Bearer {token_service.create_access_token(data={'sub': user.email})}"}
    )

    assert response.status_code == 200
    assert "subscription" in response.json()
    assert response.json()["subscription"]["author_id"] == author_id
    assert response.json()["subscription"]["subscriber_id"] == user.id
    assert "detail" in response.json()


def test_unsubscribe(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    subscription_id = "test_subscription_id"
    subscription = Subscription(id=subscription_id, author_id=2, subscriber_id=user.id)
    db_session.add(subscription)
    db_session.commit()

    response = client.delete(
        f"/subscriptions/{subscription_id}",
        headers={"Authorization": f"Bearer {token_service.create_access_token(data={'sub': user.email})}"}
    )

    assert response.status_code == 200
    assert "subscription" in response.json()
    assert response.json()["subscription"]["id"] == subscription_id
    assert "detail" in response.json()

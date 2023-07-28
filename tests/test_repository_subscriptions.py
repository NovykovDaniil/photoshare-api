from sqlalchemy.orm import Session
from src.database.models import User, Subscription
from src.repository import subscriptions
from src.messages import *
import pytest

def test_subscribe(db_session):
    user = User(id="1", username="testuser1", email="testuser1@example.com")
    author = User(id="2", username="testuser2", email="testuser2@example.com")

    db_session.add(user)
    db_session.add(author)
    db_session.commit()

    subscription = subscriptions.subscribe("2", user, db_session)
    assert subscription.subscriber_id == "1"
    assert subscription.author_id == "2"
    assert user.subscriptions == 1
    assert author.subscribers == 1

    with pytest.raises(Exception) as e:
        subscriptions.subscribe("3", user, db_session)
    assert "There is no user with such id" in str(e.value)

def test_get_subscriptions(db_session):
    user1 = User(id="1", username="testuser1", email="testuser1@example.com")
    user2 = User(id="2", username="testuser2", email="testuser2@example.com")

    db_session.add(user1)
    db_session.add(user2)
    db_session.add(Subscription(subscriber_id="1", author_id="2"))
    db_session.add(Subscription(subscriber_id="1", author_id="3"))
    db_session.add(Subscription(subscriber_id="2", author_id="1"))
    db_session.commit()

    assert len(subscriptions.get_subscriptions(user1, db_session)) == 2
    assert len(subscriptions.get_subscriptions(user2, db_session)) == 1

def test_unsubscribe(db_session):
    user1 = User(id="1", username="testuser1", email="testuser1@example.com")
    user2 = User(id="2", username="testuser2", email="testuser2@example.com")

    db_session.add(user1)
    db_session.add(user2)
    db_session.add(Subscription(subscriber_id="1", author_id="2"))
    db_session.commit()

    assert user1.subscriptions == 1
    assert user2.subscribers == 1

    subscription = subscriptions.unsubscribe("1", user1, db_session)
    assert subscription.subscriber_id == "1"
    assert subscription.author_id == "2"
    assert user1.subscriptions == 0
    assert user2.subscribers == 0

    with pytest.raises(Exception) as e:
        subscriptions.unsubscribe("2", user1, db_session)
    assert "There is no subscription with such ID or it is not your subscription" in str(e.value)

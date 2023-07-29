import unittest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app
from src.database.models import User, Subscription
from src.repository import subscriptions as repository_subscriptions

class TestSubscriptions(unittest.TestCase):

    def setUp(self) -> None:
        self.client = TestClient(app)
        self.session = MagicMock(spec=Session)
        self.author_id = 'author_id'
        self.subscription_id = 'subscription_id'
        self.user = User(id='user_id')
        self.subscription = Subscription(id=self.subscription_id)

    def test_get_subscriptions_success(self):
        repository_subscriptions.get_subscriptions = MagicMock(return_value=[self.subscription])
        response = self.client.get('/subscriptions/', headers={'Authorization': 'Bearer dummy_token'})
        self.assertEqual(response.status_code, 404)

    def test_get_subscriptions_not_found(self):
        repository_subscriptions.get_subscriptions = MagicMock(return_value=[])
        response = self.client.get('/subscriptions/', headers={'Authorization': 'Bearer dummy_token'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail': 'Not Found'})

    def test_unsubscribe_not_found(self):
        repository_subscriptions.unsubscribe = MagicMock(return_value=None)
        response = self.client.delete(f'/subscriptions/{self.subscription_id}', headers={'Authorization': 'Bearer dummy_token'})
        self.assertEqual(response.status_code, 404)


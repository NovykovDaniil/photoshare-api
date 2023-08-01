import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from src.repository.subscriptions import subscribe, get_subscriptions, unsubscribe
from src.database.models import User, Subscription

class TestSubscriptions(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.session = MagicMock(spec=Session)
        self.author_id = 'author_id'
        self.user = User(id='user_id')


    async def test_subscribe_author_not_found(self):
        self.session.query().filter().first.return_value = None

        with self.assertRaises(Exception):
            await subscribe(self.author_id, self.user, self.session)

    async def test_get_subscriptions(self):
        subscriptions = [
            Subscription(subscriber_id=self.user.id, author_id='author_id_1'),
            Subscription(subscriber_id=self.user.id, author_id='author_id_2')
        ]
        self.session.query().filter().all.return_value = subscriptions

        result = await get_subscriptions(self.user, self.session)

        self.assertEqual(result, subscriptions)

    async def test_unsubscribe_author_not_found(self):
        subscription = Subscription(subscriber_id=self.user.id, author_id=self.author_id)
        self.session.query().filter().first.return_value = subscription
        self.session.query().filter().first.side_effect = None

        with self.assertRaises(Exception):
            await unsubscribe(subscription.id, self.user, self.session)


import unittest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import MagicMock

from src.database.models import Tag
from src.schemas import TagModel
from src.repository.tags import create_tag, is_exists
from main import app


class TestTags(unittest.TestCase):

    def setUp(self) -> None:
        self.client = TestClient(app)
        self.session = MagicMock(spec=Session)
        self.tag_model = TagModel(tag='test')

    def test_create_tag_success(self):
        create_tag_mock = MagicMock(return_value=Tag(id=1, name='test'))
        is_exists_mock = MagicMock(return_value=False)
        create_tag.side_effect = create_tag_mock
        is_exists.side_effect = is_exists_mock

        response = self.client.post('/tags/', json=self.tag_model.dict())

        self.assertEqual(response.status_code, 404)


    def test_create_tag_conflict(self):
        create_tag_mock = MagicMock(return_value=Tag(id=1, name='test'))
        is_exists_mock = MagicMock(return_value=True)
        create_tag.side_effect = create_tag_mock
        is_exists.side_effect = is_exists_mock

        response = self.client.post('/tags/', json=self.tag_model.dict())

        self.assertEqual(response.status_code, 404)
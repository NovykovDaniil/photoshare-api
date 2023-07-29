import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Tag
from src.schemas import TagModel
from src.repository.tags import create_tag, is_exists


class TestTags(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.session = MagicMock(spec=Session)
        self.tag = Tag(id = 1, name = 'test')
    
    async def test_create_tag(self):
        tag_model = TagModel(tag = self.tag.name)
        result = await create_tag(tag_model, self.session)

        self.assertEqual(result.name, self.tag.name)

    async def test_is_exists(self):
        tag_model = TagModel(tag = self.tag.name)
        self.session.query().filter().first.return_value = self.tag
        result = await is_exists(tag_model, self.session)
        
        self.assertEqual(result, True)
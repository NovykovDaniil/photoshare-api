import pytest
from unittest.mock import MagicMock
from unittest import IsolatedAsyncioTestCase
from datetime import timedelta
from datetime import datetime
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from src.database.models import User, Story, Subscription
from src.services.photos import UploadService
from src.services.role import role_service
from src.repository.stories import verify_story, get_story, create_story, delete_story, recommend
from src.constants import ONLY_VIDEO, STORY_NOT_AVALIABLE, STORY_NOT_YOUR

class TestStories(IsolatedAsyncioTestCase):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.db = MagicMock(spec=Session)
        self.user = User(id=1)
        self.file = MagicMock()

    async def test_verify_story_owner(self):
        story = Story(user_id=self.user.id)
        result = await verify_story(story, self.user)
        assert result is True

    async def test_verify_story_not_owner_not_moder(self):
        story = Story(user_id=2)
        result = await verify_story(story, self.user)
        assert result is True

    async def test_get_story_valid(self):
        story = Story(id='valid_story_id', expire_to=datetime.utcnow() + timedelta(minutes=10))
        self.db.query.return_value.filter.return_value.first.return_value = story
        result = await get_story('valid_story_id', self.db)
        assert result == story

    async def test_get_story_expired(self):
        story = Story(id='expired_story_id', expire_to=datetime.utcnow() - timedelta(minutes=10))
        self.db.query.return_value.filter.return_value.first.return_value = story
        with pytest.raises(HTTPException) as exc_info:
            await get_story('expired_story_id', self.db)
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert exc_info.value.detail == STORY_NOT_AVALIABLE

    async def test_create_story_with_invalid_file(self):
        self.file.content_type.split.return_value = ['image', 'png']
        with pytest.raises(HTTPException) as exc_info:
            await create_story(self.file, self.user, self.db)
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert exc_info.value.detail == ONLY_VIDEO



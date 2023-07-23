from pytest import mark

from src.database.models import Tag
from src.repository.tags import create_tag, is_exists


@mark.asyncio
async def test_create_tag(db_session):
    tag_name = "Test Tag"
    tag_model = {"tag": tag_name}
    tag = await create_tag(tag_model, db_session)

    assert tag is not None
    assert tag.name == tag_name


@mark.asyncio
async def test_is_exists_tag(db_session):
    tag_name = "Test Tag"
    tag = Tag(name=tag_name)
    db_session.add(tag)
    db_session.commit()

    tag_model = {"tag": tag_name}
    exists = await is_exists(tag_model, db_session)

    assert exists is True

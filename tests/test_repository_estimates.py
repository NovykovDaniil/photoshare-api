import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, Photo, User, Estimate
from src.repository.photos import get_record
from src.services.role import role_service
from src.repository.estimates import (
    is_exists_estimate,
    get_estimates,
    estimate_photo,
    delete_estimate,
    get_photo_estimates,
)

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.mark.asyncio
async def test_is_exists_estimate(db_session):
    user = User(id=1, username="test_user")
    photo_id = "photo_123"
    db_session.add(Estimate(estimate=4, photo_id=photo_id, user_id=user.id))
    db_session.commit()
    assert await is_exists_estimate(photo_id, user, db_session) is True
    assert await is_exists_estimate("non_existent_photo", user, db_session) is False

@pytest.mark.asyncio
async def test_get_estimates(db_session):
    photo_id = "photo_456"
    db_session.add(Estimate(estimate=5, photo_id=photo_id))
    db_session.add(Estimate(estimate=3, photo_id=photo_id))
    db_session.commit()
    estimates = await get_estimates(photo_id, db_session)
    assert estimates == [5, 3]
    assert await get_estimates("non_existent_photo", db_session) is None

@pytest.mark.asyncio
async def test_estimate_photo(db_session):
    user = User(id=2, username="another_user")
    photo_id = "photo_789"
    db_session.add(Photo(id=photo_id, user_id=1))
    db_session.commit()
    assert await estimate_photo(photo_id, 4, user, db_session) is not None
    assert await estimate_photo(photo_id, 3, user, db_session) is None


@pytest.mark.asyncio
async def test_get_photo_estimates(db_session):
    photo_id = "photo_654"
    db_session.add(Estimate(estimate=2, photo_id=photo_id))
    db_session.add(Estimate(estimate=1, photo_id=photo_id))
    db_session.commit()
    estimates = await get_photo_estimates(photo_id, db_session)
    assert len(estimates) == 2
    assert estimates[0].estimate == 2
    assert estimates[1].estimate == 1
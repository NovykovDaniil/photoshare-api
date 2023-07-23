from datetime import datetime
from pytest import mark

from src.database.models import User, Estimate
from src.repository.estimates import (
    is_exists_estimate,
    get_estimates,
    estimate_photo,
    delete_estimate,
)


@mark.asyncio
async def test_is_exists_estimate(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    photo_id = "test_photo_id"
    estimate = Estimate(estimate=5, photo_id=photo_id, user_id=user.id)
    db_session.add(estimate)
    db_session.commit()

    exists = await is_exists_estimate(photo_id, user, db_session)

    assert exists is True


@mark.asyncio
async def test_get_estimates(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    photo_id = "test_photo_id"
    estimates = [3, 4, 5]
    for est in estimates:
        estimate = Estimate(estimate=est, photo_id=photo_id, user_id=user.id)
        db_session.add(estimate)
    db_session.commit()

    result = await get_estimates(photo_id, db_session)

    assert isinstance(result, list)
    assert len(result) == len(estimates)
    assert all(est in result for est in estimates)


@mark.asyncio
async def test_estimate_photo(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    photo_id = "test_photo_id"
    estimate = 5

    new_estimate = await estimate_photo(photo_id, estimate, user, db_session)

    assert new_estimate is not None
    assert new_estimate.estimate == estimate
    assert new_estimate.photo_id == photo_id
    assert new_estimate.user_id == user.id
    assert isinstance(new_estimate.created_at, datetime)


@mark.asyncio
async def test_delete_estimate(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    photo_id = "test_photo_id"
    estimate = Estimate(estimate=5, photo_id=photo_id, user_id=user.id)
    db_session.add(estimate)
    db_session.commit()

    deleted_estimate = await delete_estimate(estimate.id, user, db_session)

    assert deleted_estimate is not None
    assert deleted_estimate.id == estimate.id
    assert deleted_estimate.photo_id == photo_id
    assert deleted_estimate.user_id == user.id

    assert db_session.query(Estimate).filter(Estimate.id == estimate.id).first() is None


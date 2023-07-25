from fastapi.testclient import TestClient
from pytest import fixture
from datetime import datetime
from src.database.models import User, Photo, Estimate
from src.repository.estimates import estimate_photo, get_estimates, delete_estimate
from src.schemas import EstimateModel, EstimateDeleteModel
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


def test_estimate_photo(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    photo_id = "test_photo_id"
    estimate_value = 4

    photo = Photo(id=photo_id, user_id=user.id)
    db_session.add(photo)
    db_session.commit()

    estimate = estimate_photo(EstimateModel(photo_id=photo_id, estimate=estimate_value), user, db_session)

    assert estimate is not None
    assert estimate.photo_id == photo_id
    assert estimate.user_id == user.id
    assert estimate.estimate == estimate_value
    assert isinstance(estimate.created_at, datetime)


def test_get_estimates(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    photo_id = "test_photo_id"
    estimate_value = 4

    photo = Photo(id=photo_id, user_id=user.id)
    db_session.add(photo)

    estimate1 = Estimate(photo_id=photo_id, user_id=user.id, estimate=estimate_value)
    estimate2 = Estimate(photo_id=photo_id, user_id=user.id, estimate=estimate_value)
    db_session.add_all([estimate1, estimate2])
    db_session.commit()

    estimates = get_estimates(photo_id, user, db_session)

    assert isinstance(estimates, list)
    assert len(estimates) == 2
    assert all(estimate.photo_id == photo_id for estimate in estimates)


def test_delete_estimate(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    photo_id = "test_photo_id"
    estimate_value = 4

    photo = Photo(id=photo_id, user_id=user.id)
    db_session.add(photo)

    estimate = Estimate(photo_id=photo_id, user_id=user.id, estimate=estimate_value)
    db_session.add(estimate)
    db_session.commit()

    deleted_estimate = delete_estimate(EstimateDeleteModel(estimate_id=estimate.id), user, db_session)

    assert deleted_estimate is not None
    assert deleted_estimate.id == estimate.id
    assert deleted_estimate.photo_id == photo_id
    assert deleted_estimate.user_id == user.id

    assert db_session.query(Estimate).filter(Estimate.id == estimate.id).first() is None


def test_estimate_photo_route(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    photo_id = "test_photo_id"
    estimate_value = 4

    photo = Photo(id=photo_id, user_id=user.id)
    db_session.add(photo)
    db_session.commit()

    estimate_model = EstimateModel(photo_id=photo_id, estimate=estimate_value)

    response = client.post(
        f"/estimates/{photo_id}",
        json=estimate_model.dict(),
        headers={"Authorization": f"Bearer {token_service.create_access_token(data={'sub': user.email})}"}
    )

    assert response.status_code == 200
    assert "estimate" in response.json()
    assert response.json()["estimate"]["photo_id"] == photo_id
    assert response.json()["estimate"]["user_id"] == user.id
    assert response.json()["estimate"]["estimate"] == estimate_value
    assert "detail" in response.json()


def test_get_estimates_route(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    photo_id = "test_photo_id"
    estimate_value = 4

    photo = Photo(id=photo_id, user_id=user.id)
    db_session.add(photo)

    estimate1 = Estimate(photo_id=photo_id, user_id=user.id, estimate=estimate_value)
    estimate2 = Estimate(photo_id=photo_id, user_id=user.id, estimate=estimate_value)
    db_session.add_all([estimate1, estimate2])
    db_session.commit()

    response = client.get(
        f"/estimates/{photo_id}",
        headers={"Authorization": f"Bearer {token_service.create_access_token(data={'sub': user.email})}"}
    )

    assert response.status_code == 200
    assert "estimates" in response.json()
    assert len(response.json()["estimates"]) == 2
    assert all(estimate["photo_id"] == photo_id for estimate in response.json()["estimates"])


def test_delete_estimate_route(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    photo_id = "test_photo_id"
    estimate_value = 4

    photo = Photo(id=photo_id, user_id=user.id)
    db_session.add(photo)

    estimate = Estimate(photo_id=photo_id, user_id=user.id, estimate=estimate_value)
    db_session.add(estimate)
    db_session.commit()

    estimate_delete_model = EstimateDeleteModel(estimate_id=estimate.id)

    response = client.delete(
        f"/estimates/{estimate.id}",
        json=estimate_delete_model.dict(),
        headers={"Authorization": f"Bearer {token_service.create_access_token(data={'sub': user.email})}"}
    )

    assert response.status_code == 200
    assert "estimate" in response.json()
    assert response.json()["estimate"]["id"] == estimate.id
    assert response.json()["estimate"]["photo_id"] == photo_id
    assert response.json()["estimate"]["user_id"] == user.id
    assert "detail" in response.json()

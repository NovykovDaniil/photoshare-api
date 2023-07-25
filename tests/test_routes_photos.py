from fastapi.testclient import TestClient
from pytest import fixture
from src.database.models import User, Photo
from src.repository.photos import create_photo, delete_photo, edit_description, search_photos, get_record, add_tags, add_filter
from src.schemas import PhotoModel, PhotoEditModel, PhotoTagModel, PhotoFilterModel
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


def test_create_photo(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    file_content = b"test_file_content"
    file = ("test_image.jpg", file_content)

    response = client.post(
        "/photos/",
        files={"file": file},
        data={"description": "Test description", "tags": "tag1,tag2"},
        headers={"Authorization": f"Bearer {token_service.create_access_token(data={'sub': user.email})}"}
    )

    assert response.status_code == 201
    assert "photo" in response.json()
    assert response.json()["photo"]["user_id"] == user.id
    assert "detail" in response.json()


def test_delete_photo(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    photo_id = "test_photo_id"
    photo = Photo(id=photo_id, user_id=user.id)
    db_session.add(photo)
    db_session.commit()

    response = client.delete(
        f"/photos/{photo_id}",
        headers={"Authorization": f"Bearer {token_service.create_access_token(data={'sub': user.email})}"}
    )

    assert response.status_code == 200
    assert "photo" in response.json()
    assert response.json()["photo"]["id"] == photo_id
    assert "detail" in response.json()


def test_edit_description(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    photo_id = "test_photo_id"
    description = "Test description"

    photo = Photo(id=photo_id, user_id=user.id)
    db_session.add(photo)
    db_session.commit()

    edit_model = PhotoEditModel(photo_id=photo_id, description=description)

    response = client.put(
        f"/photos/{photo_id}",
        json=edit_model.dict(),
        headers={"Authorization": f"Bearer {token_service.create_access_token(data={'sub': user.email})}"}
    )

    assert response.status_code == 200
    assert "photo" in response.json()
    assert response.json()["photo"]["id"] == photo_id
    assert response.json()["photo"]["description"] == description
    assert "detail" in response.json()


def test_search_photos(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    photo_id1 = "test_photo_id1"
    photo_id2 = "test_photo_id2"

    photo1 = Photo(id=photo_id1, user_id=user.id)
    photo2 = Photo(id=photo_id2, user_id=user.id)
    db_session.add_all([photo1, photo2])
    db_session.commit()

    response = client.get(
        "/photos/",
        params={"tag": "tag1", "keyword": "keyword"},
        headers={"Authorization": f"Bearer {token_service.create_access_token(data={'sub': user.email})}"}
    )

    assert response.status_code == 200
    assert "photos" in response.json()
    assert len(response.json()["photos"]) == 2
    assert all(photo["user_id"] == user.id for photo in response.json()["photos"])


def test_get_record(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    photo_id = "test_photo_id"

    photo = Photo(id=photo_id, user_id=user.id)
    db_session.add(photo)
    db_session.commit()

    response = client.get(
        f"/photos/{photo_id}",
        headers={"Authorization": f"Bearer {token_service.create_access_token(data={'sub': user.email})}"}
    )

    assert response.status_code == 200
    assert "photo" in response.json()
    assert response.json()["photo"]["id"] == photo_id
    assert response.json()["photo"]["user_id"] == user.id
    assert "detail" in response.json()


def test_add_tags(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    photo_id = "test_photo_id"

    photo = Photo(id=photo_id, user_id=user.id)
    db_session.add(photo)
    db_session.commit()

    tag_model = PhotoTagModel(photo_id=photo_id, tags=["tag1", "tag2"])

    response = client.put(
        f"/photos/{photo_id}/tags",
        json=tag_model.dict(),
        headers={"Authorization": f"Bearer {token_service.create_access_token(data={'sub': user.email})}"}
    )

    assert response.status_code == 200
    assert "photo" in response.json()
    assert response.json()["photo"]["id"] == photo_id
    assert all(tag.name in ["tag1", "tag2"] for tag in response.json()["photo"]["tags"])
    assert "detail" in response.json()


def test_add_filter(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    photo_id = "test_photo_id"

    photo = Photo(id=photo_id, user_id=user.id)
    db_session.add(photo)
    db_session.commit()

    filter_model = PhotoFilterModel(photo_id=photo_id, filtername="test_filter")

    response = client.put(
        f"/photos/{photo_id}/filter",
        json=filter_model.dict(),
        headers={"Authorization": f"Bearer {token_service.create_access_token(data={'sub': user.email})}"}
    )

    assert response.status_code == 200
    assert "photo" in response.json()
    assert response.json()["photo"]["id"] == photo_id
    assert "detail" in response.json()

from fastapi.testclient import TestClient
from pytest import fixture

from src.services.photos import UploadService
from src.database.db import get_db
from main import app

client = TestClient(app)


@fixture(scope="function")
def db_session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


def test_create_name():
    email = "test@example.com"
    prefix = "photos"
    expected_name = "photos/96c2f7e7a198"

    photo_name = UploadService.create_name(email, prefix)

    assert photo_name == expected_name


def test_upload():
    file = b"test_image_data"
    public_id = "test_public_id"

    response = UploadService.upload(file, public_id)
    assert response is not None


def test_get_url():
    public_id = "test_public_id"
    version = "test_version"
    width = 200
    height = 200

    url = UploadService.get_url(public_id, version, width, height)
    assert url is not None


def test_add_filter():
    url = "https://test_cloudinary_url"
    filtername = "test_filter"

    transformed_image_url = UploadService.add_filter(url, filtername)

    assert transformed_image_url is not None

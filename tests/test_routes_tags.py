from fastapi.testclient import TestClient
from pytest import fixture
from src.database.models import Tag
from src.repository.tags import is_exists, create_tag
from src.schemas import TagModel, TagResponse
from main import app

client = TestClient(app)


@fixture(scope="function")
def db_session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


def test_create_tag(db_session):
    tag_name = "test_tag"

    response = client.post(
        "/tags/",
        json={"name": tag_name},
    )

    assert response.status_code == 201
    assert "tag" in response.json()
    assert response.json()["tag"]["name"] == tag_name
    assert "details" in response.json()

    db_tag = db_session.query(Tag).filter(Tag.name == tag_name).first()
    assert db_tag is not None
    assert db_tag.name == tag_name


def test_create_existing_tag(db_session):
    tag_name = "existing_tag"

    existing_tag = Tag(name=tag_name)
    db_session.add(existing_tag)
    db_session.commit()

    response = client.post(
        "/tags/",
        json={"name": tag_name},
    )

    assert response.status_code == 409
    assert "detail" in response.json()
    assert response.json()["detail"] == "Tag already exists"

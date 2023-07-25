from fastapi.testclient import TestClient
from pytest import fixture
from datetime import datetime
from src.database.models import User, Comment
from src.repository.comments import create_comment, edit_comment, delete_comment, get_comments
from src.schemas import CommentModel, CommentEditModel
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


def test_create_comment(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    photo_id = "test_photo_id"
    text = "Test comment text"

    comment = create_comment(photo_id, text, user, db_session)

    assert comment is not None
    assert comment.photo_id == photo_id
    assert comment.user_id == user.id
    assert comment.text == text
    assert isinstance(comment.created_at, datetime)


def test_edit_comment(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)

    photo_id = "test_photo_id"
    text = "Test comment text"

    comment = Comment(text=text, photo_id=photo_id, user_id=user.id)
    db_session.add(comment)
    db_session.commit()

    new_text = "Updated comment text"

    updated_comment = edit_comment(comment.id, new_text, user, db_session)

    assert updated_comment is not None
    assert updated_comment.id == comment.id
    assert updated_comment.photo_id == photo_id
    assert updated_comment.user_id == user.id
    assert updated_comment.text == new_text
    assert isinstance(updated_comment.updated_at, datetime)


def test_delete_comment(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)

    photo_id = "test_photo_id"
    text = "Test comment text"

    comment = Comment(text=text, photo_id=photo_id, user_id=user.id)
    db_session.add(comment)
    db_session.commit()

    deleted_comment = delete_comment(comment.id, user, db_session)

    assert deleted_comment is not None
    assert deleted_comment.id == comment.id
    assert deleted_comment.photo_id == photo_id
    assert deleted_comment.user_id == user.id

    assert db_session.query(Comment).filter(Comment.id == comment.id).first() is None


def test_get_comments(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)

    photo_id = "test_photo_id"
    text = "Test comment text"

    comment1 = Comment(text=text, photo_id=photo_id, user_id=user.id)
    comment2 = Comment(text=text, photo_id=photo_id, user_id=user.id)
    db_session.add_all([comment1, comment2])
    db_session.commit()

    comments = get_comments(photo_id, db_session)

    assert isinstance(comments, list)
    assert len(comments) == 2
    assert all(comment.photo_id == photo_id for comment in comments)


def test_create_comment_route(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    photo_id = "test_photo_id"
    text = "Test comment text"

    comment_model = CommentModel(photo_id=photo_id, text=text)

    response = client.post(
        f"/comments/{photo_id}",
        json=comment_model.dict(),
        headers={"Authorization": f"Bearer {token_service.create_access_token(data={'sub': user.email})}"}
    )

    assert response.status_code == 200
    assert "comment" in response.json()
    assert response.json()["comment"]["photo_id"] == photo_id
    assert response.json()["comment"]["user_id"] == user.id
    assert response.json()["comment"]["text"] == text
    assert "detail" in response.json()


def test_edit_comment_route(db_session):
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)

    photo_id = "test_photo_id"
    text = "Test comment text"

    comment = Comment(text=text, photo_id=photo_id, user_id=user.id)
    db_session.add(comment)
    db_session.commit()

    new_text = "Updated comment text"

    comment_edit_model = CommentEditModel(comment_id=comment.id, new_text=new_text)

    response = client.put(
        f"/comments/{photo_id}",
        json=comment_edit_model.dict(),
        headers={"Authorization": f"Bearer {token_service.create_access_token(data={'sub': user.email})}"}
    )

    assert response.status_code == 200
    assert "comment" in response.json()
    assert response.json()["comment"]["id"] == comment.id

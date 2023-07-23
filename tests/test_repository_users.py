from pytest import mark

from src.database.models import User
from pytest import mark

from src.database.models import User
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar,
    change_password,
    get_user,
    edit_user,
    change_user_active,
)


@mark.asyncio
async def test_get_user_by_email(db_session):
    email = "test@example.com"
    user = User(name="Test User", email=email)
    db_session.add(user)
    db_session.commit()

    result = await get_user_by_email(email, db_session)

    assert result is not None
    assert result.email == email


@mark.asyncio
async def test_create_user(db_session):
    user_model = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword",
    }
    user = await create_user(user_model, db_session)

    assert user is not None
    assert user.name == user_model["name"]
    assert user.email == user_model["email"]
    assert user.password != user_model["password"] 

@mark.asyncio
async def test_update_token(db_session):
    user = User(name="Test User", email="test@example.com", refresh_token=None)
    db_session.add(user)
    db_session.commit()

    token = "testtoken"
    await update_token(user, token, db_session)

    updated_user = db_session.query(User).filter(User.email == "test@example.com").first()

    assert updated_user.refresh_token == token


@mark.asyncio
async def test_confirmed_email(db_session):
    user = User(name="Test User", email="test@example.com", confirmed=False)
    db_session.add(user)
    db_session.commit()

    await confirmed_email("test@example.com", db_session)

    updated_user = db_session.query(User).filter(User.email == "test@example.com").first()

    assert updated_user.confirmed is True


@mark.asyncio
async def test_update_avatar(db_session):
    user = User(name="Test User", email="test@example.com", avatar=None)
    db_session.add(user)
    db_session.commit()

    avatar_url = "http://example.com/avatar.jpg"
    updated_user = await update_avatar("test@example.com", avatar_url, db_session)

    assert updated_user is not None
    assert updated_user.avatar == avatar_url


@mark.asyncio
async def test_change_password(db_session):
    user = User(name="Test User", email="test@example.com", password="oldpassword")
    db_session.add(user)
    db_session.commit()

    new_password = "newpassword"
    await change_password(user, new_password, db_session)

    updated_user = db_session.query(User).filter(User.email == "test@example.com").first()

    assert updated_user is not None
    assert updated_user.password != "oldpassword"
    assert updated_user.password == new_password


@mark.asyncio
async def test_get_user(db_session):
    user = User(name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    result = await get_user("Test User", db_session)

    assert result is not None
    assert result.name == "Test User"


@mark.asyncio
async def test_edit_user(db_session):
    user = User(name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    new_bio = "Updated bio"
    updated_user = await edit_user("Test User", new_bio, user, db_session)

    assert updated_user is not None
    assert updated_user.bio == new_bio


@mark.asyncio
async def test_change_user_active(db_session):
    user = User(name="Test User", email="test@example.com", is_active=True)
    db_session.add(user)
    db_session.commit()

    updated_user = await change_user_active("Test User", db_session)

    assert updated_user is not None
    assert updated_user.is_active is False

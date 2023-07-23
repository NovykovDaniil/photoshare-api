from sqlalchemy.orm import Session
from pytest import mark

# Импортируем функции, которые будем тестировать
from estimates import (
    is_exists_estimate,
    get_estimates,
    estimate_photo,
    delete_estimate,
)
from src.database.models import Photo, User, Estimate
from src.repository.photos import get_record
from src.messages import NO_PHOTO


@mark.asyncio
async def test_is_exists_estimate(db_session):
    """Тест функции is_exists_estimate."""

    # Создаем тестовые данные
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)

    photo_id = "test_photo_id"

    # Создаем оценку для тестирования
    estimate = Estimate(estimate=5, photo_id=photo_id, user_id=user.id)
    db_session.add(estimate)
    db_session.commit()

    # Вызываем тестируемую функцию
    result = await is_exists_estimate(photo_id, user, db_session)

    # Проверяем результаты
    assert result is True


@mark.asyncio
async def test_get_estimates(db_session):
    """Тест функции get_estimates."""

    # Создаем тестовые данные
    photo_id = "test_photo_id"

    # Создаем оценки для тестирования
    estimates = [5, 4, 3, 2, 5]
    db_estimates = [Estimate(estimate=est, photo_id=photo_id) for est in estimates]
    db_session.add_all(db_estimates)
    db_session.commit()

    # Вызываем тестируемую функцию
    result = await get_estimates(photo_id, db_session)

    # Проверяем результаты
    assert result == estimates


@mark.asyncio
async def test_estimate_photo(db_session):
    """Тест функции estimate_photo."""

    # Создаем тестовые данные
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)

    photo_id = "test_photo_id"
    estimate = 5

    # Создаем фото для тестирования
    photo = Photo(id=photo_id, user_id=2, raiting=0)  # Не совпадает user_id, чтобы тест был корректным
    db_session.add(photo)
    db_session.commit()

    # Вызываем тестируемую функцию
    result = await estimate_photo(photo_id, estimate, user, db_session)

    # Проверяем результаты
    assert result is not None
    assert result.estimate == estimate

    # Проверяем, что оценка учтена в рейтинге фото
    photo = db_session.query(Photo).filter(Photo.id == photo_id).first()
    assert photo.raiting == estimate


@mark.asyncio
async def test_delete_estimate(db_session):
    """Тест функции delete_estimate."""

    # Создаем тестовые данные
    user = User(id=1, name="Test User", email="test@example.com")
    db_session.add(user)

    photo_id = "test_photo_id"
    estimate = Estimate(estimate=5, photo_id=photo_id, user_id=user.id)
    db_session.add(estimate)
    db_session.commit()

    # Вызываем тестируемую функцию
    result = await delete_estimate(estimate.id, user, db_session)

    # Проверяем результаты
    assert result is not None
    assert result.id == estimate.id

    # Проверяем, что оценка удалена из базы данных
    assert db_session.query(Estimate).filter(Estimate.id == estimate.id).first() is None

    # Проверяем, что оценка учтена в рейтинге фото
    photo = db_session.query(Photo).filter(Photo.id == photo_id).first()
    assert photo.raiting == 0


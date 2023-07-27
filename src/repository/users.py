from libgravatar import Gravatar
from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from src.database.models import User, UserRole
from src.services.role import role_service
from src.schemas import UserModel
from src.messages import *


async def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    avatar = None
    try:
        gr = Gravatar(body.email)
        avatar = gr.get_image()
    except Exception as err:
        print(err)
    new_user = User(**dict(body), avatar=avatar)
    is_first_user = db.query(User).first()
    if is_first_user is None:
        new_user.role = UserRole.ADMIN
        new_user.confirmed = True
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user


async def change_password(user: User, new_password: str, db: Session) -> None:
    user.password = new_password
    db.commit()


async def get_user(username: str, db: Session) -> User:
    user = db.query(User).filter(User.username == username).first()
    return user


async def edit_user(username: str, bio: str, user: User, db: Session) -> User:
    user_ = await get_user(username, db)
    if user_.username != user.username or not await role_service.is_admin(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=NOT_YOUR_ACCOUNT
        )
    user_.bio = bio
    db.add(user_)
    db.commit()
    db.refresh(user_)
    return user_


async def change_user_active(username: str, user: User, db: Session):
    user_ = await get_user(username, db)
    if await role_service.is_admin(user):
        user_.is_active = not user_.is_active
        db.add(user_)
        db.commit()
        db.refresh(user_)
        return user_
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=NO_PERMISSIONS)
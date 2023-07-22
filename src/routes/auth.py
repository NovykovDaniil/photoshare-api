import random
import string

from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status,
    Security,
    BackgroundTasks,
    Request,
)
from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import (
    UserModel,
    UserResponse,
    TokenModel,
    RequestEmail,
    ChangePassword,
    UserResetPassword,
)

from src.repository import users as repository_users
from src.services.auth import password_service, token_service
from src.services.email import send_email_confirmation, send_email_reset
from src.messages import *


router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


def generate_reset_code():
    reset_code = "".join(random.choices(string.digits, k=5))
    return reset_code


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    body: UserModel,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=ACCOUNT_EXISTS)
    is_exists_name = db.query(User).filter(User.username == body.username).first()
    if is_exists_name:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=USERNAME_EXISTS
        )
    body.password = password_service.hash_password(body.password)
    new_user = await repository_users.create_user(body, db)
    background_tasks.add_task(send_email_confirmation, new_user.email, new_user.username, request.base_url)
    return {
        "user": new_user,
        "detail": USER_CREATED,
    }


@router.post("/login", response_model=TokenModel)
async def login(
    body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_EMAIL
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=BANNED)
    if not user.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=NOT_CONFIRMED
        )
    if not password_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_PASSWORD
        )
    access_token = await token_service.create_access_token(data={"sub": user.email})
    refresh_token = await token_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/logout")
async def logout(
    token: str = Depends(token_service.oauth2_scheme),
):
    await token_service.ban_access_token(token)
    return {"message": LOGGED_OUT}


@router.get("/refresh_token", response_model=TokenModel)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    email = await token_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_REFRESH_TOKEN
        )

    access_token = await token_service.create_access_token(data={"sub": email})
    refresh_token = await token_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/confirmed_email/{token}")
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    email = await token_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=VERIFICATION_ERROR
        )
    if user.confirmed:
        return {"message": EMAIL_ALREADY_CONFIRMED}
    await repository_users.confirmed_email(email, db)
    return {"message": EMAIL_CONFIRMED}


@router.post("/request_email")
async def request_email(
    body: RequestEmail,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
    _: HTTPAuthorizationCredentials = Security(security),
):
    user = await repository_users.get_user_by_email(body.email, db)
    if user.confirmed:
        return {"message": EMAIL_ALREADY_CONFIRMED}
    if user:
        background_tasks.add_task(
            send_email_confirmation, user.email, user.username, request.base_url
        )
    return {"message": CHECK_EMAIL}


@router.post("/request_reset_password")
async def request_reset_password(
    body: RequestEmail, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    user = await repository_users.get_user_by_email(body.email, db)
    if user:
        reset_code = generate_reset_code()
        background_tasks.add_task(send_email_reset, user.email, reset_code)
        user.reset_code = reset_code
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"message": RESET_CODE_CHECK}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=USER_NOT_FOUND,
    )


@router.post("/reset_password", response_model=UserResponse)
async def reset_password(
    body: UserResetPassword, db: Session = Depends(get_db)
) -> User:
    user = await repository_users.get_user_by_email(body.email, db)
    if user:
        if user.reset_code == body.reset_code:
            user.password = password_service.hash_password(body.new_password)
            user.reset_code = None
            db.add(user)
            db.commit()
            db.refresh(user)
            return {"user": user, "detail": PASSWORD_CHANGED}
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=WRONG_RESET_CODE
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=USER_NOT_FOUND,
    )


@router.post("/change_password")
async def change_password(
    body: ChangePassword,
    db: Session = Depends(get_db),
    _: HTTPAuthorizationCredentials = Security(security),
):
    user = await repository_users.get_user_by_email(body.email, db)
    if user:
        if body.current_password == body.new_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=SAME_PASSWORDS
            )
        if password_service.verify_password(body.current_password, user.password):
            hashed_new_password = password_service.hash_password(body.new_password)
            await repository_users.change_password(user, hashed_new_password, db)
            return {"message": PASSWORD_CHANGED}
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=WRONG_PASSWORD
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=USER_NOT_FOUND,
    )


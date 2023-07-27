import redis.asyncio as redis
import secrets
import jwt
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from functools import wraps
from fastapi.responses import JSONResponse
from src.routes import auth, tags, photos, users, comments, estimates, subscriptions, stories
from src.database.models import UserRole

app = FastAPI()
security = HTTPBearer()
# Sample secret key to decode the token (for demonstration purposes)
SECRET_KEY = secrets.token_hex(32)  # 32 bytes -> 64 hexadecimal characters

app.include_router(auth.router, prefix="/api")
app.include_router(tags.router, prefix="/api")
app.include_router(photos.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(comments.router, prefix="/api")
app.include_router(estimates.router, prefix="/api")
app.include_router(subscriptions.router, prefix="/api")
app.include_router(stories.router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hi! Welcome to the photo share!"}


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_user_role_from_db(token):
    payload = verify_token(token)
    return payload.get("role", None)


def check_role(token, role_to_check):
    # Check if the user role matches the given role_to_check
    user_role = get_user_role_from_db(token)
    return user_role == role_to_check


def has_role(role: UserRole):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            credentials: HTTPAuthorizationCredentials = Depends(security)
            token = credentials.credentials

            if check_role(token, role):
                return func(*args, **kwargs)
            else:
                raise HTTPException(status_code=403, detail="Forbidden")

        return wrapper

    return decorator


@app.get("/admin", tags=["admin"])
@has_role(UserRole.ADMIN)
async def admin_route():
    return JSONResponse(content={"message": "Hello, Admin!"})


@app.get("/user", tags=["user"])
@has_role(UserRole.USER)
async def user_route():
    return JSONResponse(content={"message": "Hello, User!"})


@app.get("/moderator", tags=["moderator"])
@has_role(UserRole.MODERATOR)
async def moderator_route():
    return JSONResponse(content={"message": "Hello, Moderator!"})

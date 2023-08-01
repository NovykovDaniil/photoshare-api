import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter

from src.routes import auth, tags, photos, users, comments, estimates, subscriptions, stories, chats, messages, models
from src.conf.config import settings


app = FastAPI()

app.include_router(auth.router, prefix="/api")
app.include_router(tags.router, prefix="/api")
app.include_router(photos.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(comments.router, prefix="/api")
app.include_router(estimates.router, prefix="/api")
app.include_router(subscriptions.router, prefix="/api")
app.include_router(stories.router, prefix="/api")
app.include_router(chats.router, prefix="/api")
app.include_router(messages.router, prefix="/api")
app.include_router(models.router, prefix="/api")


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=settings.redis_host,
                          port=settings.redis_port, 
                          password=settings.redis_password,
                          db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)
    

@app.get("/")
def read_root():
    return {"message": "Hi! Welcome to the photo share!"}

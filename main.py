import redis.asyncio as redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import auth, tags, photos, users, comments, estimates


app = FastAPI()


app.include_router(auth.router, prefix="/api")
# app.include_router(tags.router, prefix="/api")
# app.include_router(photos.router, prefix="/api")
# app.include_router(users.router, prefix="/api")
# app.include_router(comments.router, prefix="/api")
# app.include_router(estimates.router, prefix="/api")


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

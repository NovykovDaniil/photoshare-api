from fastapi import (
    APIRouter,
    Depends,
)
from fastapi_limiter.depends import RateLimiter

from src.schemas import (
    GPTModel,
    GPTImageModel,
    GPTImageResponse,
    GPTResponse,
)
from src.database.models import User
from src.repository import models as repository_models
from src.services.auth import token_service
from src.constants import *


router = APIRouter(prefix="/models", tags=["models"])


@router.post('/dall-e/images', response_model=GPTImageResponse, dependencies=[Depends(RateLimiter(times=1, seconds=120))])
async def generate_image(body: GPTImageModel, _: User = Depends(token_service.get_current_user)):
    image_url = await repository_models.generate_image(body.description)
    return {'url': image_url}





from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import (
    EstimateModel,
    EstimateResponse,
    EstimatesResponse,
    EstimateDeleteModel,
)
from src.database.models import User
from src.repository import estimates as repository_estimates
from src.services.auth import token_service
from src.messages import *


router = APIRouter(prefix="/estimates", tags=["estimates"])


@router.post("/{photo_id}", response_model=EstimateResponse)
async def estimate_photo(
    body: EstimateModel,
    user: User = Depends(token_service.get_current_user),
    db: Session = Depends(get_db),
):
    estimate = await repository_estimates.estimate_photo(
        body.photo_id, body.estimate, user, db
    )
    if estimate is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ESTIMATE_EXISTS_OR_YOUR_PHOTO,
        )
    return {"estimate": estimate, "detail": PHOTO_ESTIMATED}


@router.get("/{photo_id}", response_model=EstimatesResponse)
async def get_estimates(
    photo_id: str,
    user: User = Depends(token_service.get_current_user),
    db: Session = Depends(get_db),
):
    estimates = await repository_estimates.get_photo_estimates(photo_id, db)
    if estimates is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ESTIMATES_NOT_FOUND
        )
    return {"estimates": estimates, "detail": ESTIMATES_FOUND}


@router.delete("/{estimate_id}", response_model=EstimateResponse)
async def delete_esitmate(
    body: EstimateDeleteModel,
    user: User = Depends(token_service.get_current_user),
    db: Session = Depends(get_db),
):
    estimate = await repository_estimates.delete_estimate(body.estimate_id, user, db)
    if estimate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_ESTIMATE)
    return {"estimate": estimate, "detail": ESTIMATE_DELETED}
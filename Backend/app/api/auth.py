from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.auth import (TokenResponse, RefreshTokenRequest,)
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    try:
        return service.login(
            email=form_data.username,
            password=form_data.password,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    try:
        return service.refresh_access_token(
            request.refresh_token
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

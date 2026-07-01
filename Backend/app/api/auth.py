from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import AuthService

router= APIRouter(
        prefix="/auth",
        tags=["Authentication"],
        )

@router.post(
        "/login",
        response_model=TokenResponse,
)

def login(
        login_data:LoginRequest,
        db:Session=Depends(get_db),
):
    service=AuthService(db)

    try:
        return service.login(login_data)

    except ValueError as e:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
        )



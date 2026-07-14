from fastapi import APIRouter, Depends, Query, BackgroundTasks
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.auth import (
    TokenResponse,
    RefreshTokenRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    auto_error=False,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# -------------------------
# LOGIN
# -------------------------
@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    return service.login(
        email=form_data.username,
        password=form_data.password,
    )


# -------------------------
# REFRESH TOKEN
# -------------------------
@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    return service.refresh_access_token(
        request.refresh_token
    )


# -------------------------
# VERIFY EMAIL
# -------------------------
@router.get("/verify-email")
def verify_email(
    token: str = Query(...),
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    return service.verify_email(token)


# -------------------------
# FORGOT PASSWORD
# -------------------------
@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    return service.forgot_password(
        request.email,
        background_tasks,
    )


# -------------------------
# RESET PASSWORD
# -------------------------
@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    return service.reset_password(
        token=request.token,
        new_password=request.new_password,
    )


# -------------------------
# LOGOUT
# -------------------------
@router.post("/logout")
def logout(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    return service.logout(token)

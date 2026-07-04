from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session



from app.db.dependencies import get_db

from app.dependencies.auth import get_current_user



from app.models.user import User



from app.schemas.api_key import (

        APIKeyCreate,

        APIKeyResponse,

        APIKeyListResponse,

        )



from app.services.api_key_service import APIKeyService





router = APIRouter(

        prefix="/api-keys",

        tags=["API Keys"],

        )





# -------------------------

# Create API Key

# -------------------------

@router.post(

        "/",

        response_model=APIKeyResponse,

        status_code=status.HTTP_201_CREATED,

        )

def create_api_key(

        request: APIKeyCreate,

        current_user: User = Depends(get_current_user),

        db: Session = Depends(get_db),

        ):

    service = APIKeyService(db)



    try:

        return service.create_api_key(

                current_user=current_user,

                request=request,

                )



    except ValueError as e:

        raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail=str(e),

                )





# -------------------------

# List API Keys

# -------------------------

@router.get(

        "/",

        response_model=list[APIKeyListResponse],

        )

def list_api_keys(

        current_user: User = Depends(get_current_user),

        db: Session = Depends(get_db),

        ):

    service = APIKeyService(db)



    return service.list_api_keys(current_user)





# -------------------------

# Revoke API Key

# -------------------------

@router.delete("/{api_key_id}")

def revoke_api_key(

        api_key_id: int,

        current_user: User = Depends(get_current_user),

        db: Session = Depends(get_db),

        ):

    service = APIKeyService(db)



    try:

        return service.revoke_api_key(

                api_key_id,

                current_user,

                )



    except ValueError as e:

        raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail=str(e),

                )

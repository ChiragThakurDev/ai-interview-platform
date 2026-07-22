from fastapi import Depends, HTTPException, status

from app.models.api_key import APIKey
from app.dependencies.api_key import get_current_api_key


def require_permission(permission: str):
    def dependency(
        api_key: APIKey = Depends(get_current_api_key),
    ):
        permissions = [
            p.strip().lower()
            for p in api_key.permissions.split(",")
        ]

        if permission.lower() not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"'{permission}' permission required.",
            )

        return api_key

    return dependency

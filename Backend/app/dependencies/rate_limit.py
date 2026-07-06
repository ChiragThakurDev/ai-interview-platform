from fastapi import Depends, HTTPException, status

from app.dependencies.api_key import get_api_key_user

from app.models.api_key import APIKey
 
from app.db.redis import redis_client


def rate_limit(
        max_requests:int,
        window:int,
):
    def dependency(
            api_key:APIKey=Depends(get_api_key_user),
    ):
        redis_key=f"rate_limit:{api_key.id}"

        current_requests=redis_client.incr(redis_key)

        if current_requests ==1:
            redis_client.expire(redis_key,window)

        if current_requests > max_requests:
            raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded. Please try again later.",
                )
        return api_key

    return dependency


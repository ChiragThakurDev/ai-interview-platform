from app.db.redis import redis_client


def store_refresh_token(
    token: str,
    expires_in: int,
):
    """
    Store a refresh token in Redis.
    """
    redis_client.setex(
        f"refresh:{token}",
        expires_in,
        "valid",
    )


def is_refresh_token_valid(
    token: str,
) -> bool:
    """
    Check whether the refresh token exists in Redis.
    """
    return redis_client.exists(
        f"refresh:{token}"
    ) == 1


def delete_refresh_token(
    token: str,
):
    """
    Delete a refresh token from Redis.
    """
    redis_client.delete(
        f"refresh:{token}"
    )


def rotate_refresh_token(
    old_token: str,
    new_token: str,
    expires_in: int,
):
    """
    Delete the old refresh token and store the new one.
    """
    delete_refresh_token(old_token)
    store_refresh_token(
        new_token,
        expires_in,
    )

from app.db.redis import redis_client


def blacklist_token(token: str, expires_in: int):
    redis_client.setex(
        token,
        expires_in,
        "blacklisted",
    )


def is_token_blacklisted(token: str):
    return redis_client.exists(token) == 1

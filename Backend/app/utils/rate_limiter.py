from app.db.redis import redis_client

MAX_LOGIN_ATTEMPTS = 5
LOCK_TIME = 900  # 15 minutes


def get_login_key(email: str):
    return f"login_attempts:{email}"


def increment_login_attempts(email: str):
    key = get_login_key(email)

    attempts = redis_client.incr(key)

    if attempts == 1:
        redis_client.expire(key, LOCK_TIME)

    return attempts


def get_login_attempts(email: str):
    key = get_login_key(email)

    attempts = redis_client.get(key)

    if attempts is None:
        return 0

    return int(attempts)


def reset_login_attempts(email: str):
    key = get_login_key(email)

    redis_client.delete(key)


def is_login_blocked(email: str):
    return get_login_attempts(email) >= MAX_LOGIN_ATTEMPTS

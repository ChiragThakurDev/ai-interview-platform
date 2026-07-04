import secrets
import hashlib


def generate_api_key() -> str:
    """
    Generate a secure random API key.
    """
    return secrets.token_urlsafe(32)


def hash_api_key(api_key: str) -> str:
    """
    Hash the API key before storing it.
    """
    return hashlib.sha256(api_key.encode()).hexdigest()


def verify_api_key(api_key: str, hashed_key: str) -> bool:
    """
    Verify an API key against its stored hash.
    """
    return hash_api_key(api_key) == hashed_key

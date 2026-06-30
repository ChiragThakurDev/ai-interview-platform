from app.utils.security import (
    hash_password,
    verify_password,
)

password = "chirag123"

hashed = hash_password(password)

print("Original :", password)
print("Hash     :", hashed)

print(
    verify_password(
        "chirag123",
        hashed
    )
)

print(
    verify_password(
        "wrongpassword",
        hashed
    )
)

from app.utils.jwt import (
    create_email_verification_token,
    verify_access_token,
)

token = create_email_verification_token(
    {
        "sub": "rahul123@gmail.com",
    }
)

print("TOKEN:")
print(token)

print("\nPAYLOAD:")
print(verify_access_token(token))

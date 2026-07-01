from app.utils.jwt import create_access_token, verify_access_token

data = {
    "sub": "chirag@gmail.com"
}

token = create_access_token(data)

print("Generated Token:")
print(token)

payload = verify_access_token(token)

print("\nDecoded Payload:")
print(payload)

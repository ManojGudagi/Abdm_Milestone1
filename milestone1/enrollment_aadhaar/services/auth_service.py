# services/auth_service.py

from milestone1.enrollment_aadhaar.services.jwt_service import (
    generate_access_token,
    generate_refresh_token
)
import uuid


# simple in-memory token store
TOKENS = set()

def generate_token():
    token = str(uuid.uuid4())
    TOKENS.add(token)
    return token

def validate_token(token):
    return token in TOKENS

def create_session(data):
    # ✅ Validate grant type
    if data.get("grantType") != "client_credentials":
        return {"error": "invalid_grant"}, 400

    # ✅ Validate client (mock)
    if data.get("clientId") != "sbx_client" or data.get("clientSecret") != "sbx_secret":
        return {"error": "invalid_client"}, 401

    access_token = generate_access_token(data["clientId"])
    refresh_token = generate_refresh_token(data["clientId"])

    return {
        "accessToken": access_token,
        "expiresIn": 1200,
        "refreshExpiresIn": 1800,
        "refreshToken": refresh_token,
        "tokenType": "bearer"
    }, 200
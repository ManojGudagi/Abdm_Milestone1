import jwt
import datetime
import uuid

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"


def generate_access_token(client_id):
    payload = {
        "sub": client_id,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=1200),
        "jti": str(uuid.uuid4()),
        "type": "access"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def generate_refresh_token(client_id):
    payload = {
        "sub": client_id,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=1800),
        "jti": str(uuid.uuid4()),
        "type": "refresh"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# ✅ ADD THIS FUNCTION
def verify_token(token: str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded

    except jwt.ExpiredSignatureError:
        return None   # token expired

    except jwt.InvalidTokenError:
        return None   # invalid token
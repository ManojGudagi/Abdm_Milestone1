import base64
from datetime import datetime, timezone
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from django.core.cache import cache

def get_abdm_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")

def encrypt_abdm_data(plaintext: str) -> str:
    if not plaintext:
        return ""

    public_key_pem = b"""-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAstWB95C5pHLXiYW59qyO4Xb+59KYVm9Hywbo77qETZVAyc6VIsxU+UWhd/k/YtjZibCznB+HaXWX9TVTFs9Nwgv7LRGq5uLczpZQDrU7dnGkl/urRA8p0Jv/f8T0MZdFWQgks91uFffeBmJOb58u68ZRxSYGMPe4hb9XXKDVsgoSJaRNYviH7RgAI2QhTCwLEiMqIaUX3p1SAc178ZlN8qHXSSGXvhDR1GKM+y2DIyJqlzfik7lD14mDY/I4lcbftib8cv7llkybtjX1AayfZp4XpmIXKWv8nRM488/jOAF81Bi13paKgpjQUUuwq9tb5Qd/DChytYgBTBTJFe7irDFCmTIcqPr8+IMB7tXA3YXPp3z605Z6cGoYxezUm2Nz2o6oUmarDUntDhq/PnkNergmSeSvS8gD9DHBuJkJWZweG3xOPXiKQAUBr92mdFhJGm6fitO5jsBxgpmulxpG0oKDy9lAOLWSqK92JMcbMNHn4wRikdI9HSiXrrI7fLhJYTbyU3I4v5ESdEsayHXuiwO/1C8y56egzKSw44GAtEpbAkTNEEfK5H5R0QnVBIXOvfeF4tzGvmkfOO6nNXU3o/WAdOyV3xSQ9dqLY5MEL4sJCGY1iJBIAQ452s8v0ynJG5Yq+8hNhsCVnklCzAlsIzQpnSVDUVEzv17grVAw078CAwEAAQ==
-----END PUBLIC KEY-----"""

    public_key = load_pem_public_key(public_key_pem)

    ciphertext = public_key.encrypt(
        plaintext.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None
        )
    )
    return base64.b64encode(ciphertext).decode('utf-8')

def get_abdm_access_token() -> str:
    return cache.get("abdm_gateway_token")

def get_user_x_token() -> str:
    token = cache.get("x_token")
    if token:
        if not token.startswith("Bearer "):
            return f"Bearer {token}"
        return token
    return None

# ✅ Add this new import at the top of your utils.py file
from rest_framework.permissions import BasePermission

# ... (keep all your existing encryption and token functions) ...

class HasGatewayToken(BasePermission):
    """
    Custom DRF Permission: Blocks the API View from executing if the 
    Gateway Token is missing or expired in the Django cache.
    """
    # This is the exact error message Swagger will show if they are blocked
    message = "Gateway token is missing or expired. Please run the Milestone 2 Auth Token API (/api_m2/v2/gateway/sessions/) first."

    def has_permission(self, request, view):
        # The bouncer checks the cache. 
        # If token exists -> Returns True (Let them in)
        # If token is None -> Returns False (Kick them out)
        return cache.get("abdm_gateway_token") is not None
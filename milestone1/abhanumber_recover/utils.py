# milestone1/abhanumber_recover/utils.py

import base64
import requests
from datetime import datetime, timezone
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from django.core.cache import cache

def get_abdm_timestamp():
    """Generates the strict ISO 8601 timestamp required by ABDM v3 APIs."""
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")

def encrypt_abdm_data(plaintext: str) -> str:
    """
    Encrypts data using RSA/ECB/OAEPWithSHA-1AndMGF1Padding.
    """
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

def fetch_new_gateway_token() -> str:
    """
    Calls the ABDM Sessions API to generate a brand new token.
    """
    url = "https://dev.abdm.gov.in/gateway/v0.5/sessions" 
    
    # ⚠️ Replace these with your actual ABDM Sandbox credentials
    payload = {
        "clientId": "SBXID_011854",
        "clientSecret": "67783361-89dc-4b83-98c5-f77b85e6e122"
    }
    
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status() 
        data = response.json()
        
        access_token = data.get("accessToken")
        
        # Save this token in Django's cache for 15 minutes
        cache.set("abdm_gateway_token", access_token, timeout=900)
        
        return access_token
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch ABDM token: {e}")
        return ""

def get_abdm_access_token() -> str:
    """
    Smart token fetcher. Checks cache first, generates new one if missing.
    """
    token = cache.get("abdm_gateway_token")
    
    if token:
        return token
        
    return fetch_new_gateway_token()
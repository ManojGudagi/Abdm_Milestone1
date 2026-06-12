import base64
import uuid
import requests
from datetime import datetime, timezone
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key

def get_abdm_timestamp():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")

def encrypt_abdm_data(plaintext: str) -> str:
    if not plaintext: return ""
    public_key_pem = b"""-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAstWB95C5pHLXiYW59qyO4Xb+59KYVm9Hywbo77qETZVAyc6VIsxU+UWhd/k/YtjZibCznB+HaXWX9TVTFs9Nwgv7LRGq5uLczpZQDrU7dnGkl/urRA8p0Jv/f8T0MZdFWQgks91uFffeBmJOb58u68ZRxSYGMPe4hb9XXKDVsgoSJaRNYviH7RgAI2QhTCwLEiMqIaUX3p1SAc178ZlN8qHXSSGXvhDR1GKM+y2DIyJqlzfik7lD14mDY/I4lcbftib8cv7llkybtjX1AayfZp4XpmIXKWv8nRM488/jOAF81Bi13paKgpjQUUuwq9tb5Qd/DChytYgBTBTJFe7irDFCmTIcqPr8+IMB7tXA3YXPp3z605Z6cGoYxezUm2Nz2o6oUmarDUntDhq/PnkNergmSeSvS8gD9DHBuJkJWZweG3xOPXiKQAUBr92mdFhJGm6fitO5jsBxgpmulxpG0oKDy9lAOLWSqK92JMcbMNHn4wRikdI9HSiXrrI7fLhJYTbyU3I4v5ESdEsayHXuiwO/1C8y56egzKSw44GAtEpbAkTNEEfK5H5R0QnVBIXOvfeF4tzGvmkfOO6nNXU3o/WAdOyV3xSQ9dqLY5MEL4sJCGY1iJBIAQ452s8v0ynJG5Yq+8hNhsCVnklCzAlsIzQpnSVDUVEzv17grVAw078CAwEAAQ==
-----END PUBLIC KEY-----"""
    public_key = load_pem_public_key(public_key_pem)
    ciphertext = public_key.encrypt(
        plaintext.encode('utf-8'),
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()), algorithm=hashes.SHA1(), label=None)
    )
    return base64.b64encode(ciphertext).decode('utf-8')

# =========================================================
# 🔍 SEARCH STEP 1: FIND ABHA ACCOUNTS (MOBILE ONLY)
# =========================================================
def search_abha_service(data, auth_header):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/abha/search"
    
    try:
        encrypted_id = encrypt_abdm_data(data.get("loginId"))
    except Exception as e:
        return {"status_code": 500, "data": {"error": f"Encryption failed: {str(e)}"}}

    # ABDM requires this endpoint to strictly use the "mobile" key
    payload = {
        "scope": ["search-abha"],
        "mobile": encrypted_id
    }

    headers = {
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "Authorization": auth_header
    }

    response = requests.post(url=url, json=payload, headers=headers)
    return {"status_code": response.status_code, "data": response.json() if response.ok else response.text}

# =========================================================
# 🔍 SEARCH STEP 2: REQUEST OTP (Official Spec)
# =========================================================
def search_request_otp_service(data, auth_header):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/request/otp"
    
    try:
        # data.get("loginId") now holds your raw index string (e.g., "1")
        encrypted_index = encrypt_abdm_data(data.get("loginId"))
    except Exception as e:
        return {"status_code": 500, "data": {"error": f"Encryption failed: {str(e)}"}}

    verify_scope = "mobile-verify" if data.get("otpSystem") == "abdm" else "aadhaar-verify"

    payload = {
        "scope": ["abha-login", "search-abha", verify_scope],
        "loginHint": data.get("loginHint"), # Will safely pull "index"
        "loginId": encrypted_index,         # Your securely encrypted index
        "otpSystem": data.get("otpSystem"),
        "txnId": data.get("txnId")
    }

    headers = {
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "Authorization": auth_header
    }

    response = requests.post(url=url, json=payload, headers=headers)
    
    try:
        res_data = response.json()
    except ValueError:
        res_data = {"raw_error": response.text}
        
    return {"status_code": response.status_code, "data": res_data}

# =========================================================
# 🔍 SEARCH STEP 3: VERIFY OTP (Final Profile Token)
# =========================================================
def search_verify_otp_service(data, auth_header):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify"
    
    try:
        encrypted_otp = encrypt_abdm_data(data.get("otpValue"))
    except Exception as e:
        return {"status_code": 500, "data": {"error": f"Encryption failed: {str(e)}"}}

    verify_scope = "mobile-verify" if data.get("otpSystem") == "abdm" else "aadhaar-verify"

    payload = {
        "scope": ["abha-login", verify_scope], # Notice 'search-abha' is dropped here per docs
        "authData": {
            "authMethods": ["otp"],
            "otp": {
                "txnId": data.get("txnId"),
                "otpValue": encrypted_otp
            }
        }
    }

    headers = {
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "Authorization": auth_header
    }

    response = requests.post(url=url, json=payload, headers=headers)
    
    # No Step 4 needed! This returns the final Master Token.
    try:
        res_data = response.json()
    except ValueError:
        res_data = {"raw_error": response.text}
        
    return {"status_code": response.status_code, "data": res_data}
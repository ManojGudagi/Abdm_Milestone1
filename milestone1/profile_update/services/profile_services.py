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

# Helper dictionary to map your action to the government's exact scopes
SCOPE_MAP = {
    'update-mobile': ["abha-profile", "mobile-verify"],
    'delete': ["abha-profile", "delete"],
    'deactivate': ["abha-profile", "de-activate"],
    're-kyc': ["abha-profile", "re-kyc"]
}

# =========================================================
# ⚙️ STEP 1: REQUEST OTP FOR ANY PROFILE ACTION
# =========================================================
def profile_request_otp_service(data, auth_header, x_token):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/request/otp"

    # 🧹 Clean the ID (Remove hyphens to prevent gateway parsing errors)
    clean_id = data.get("loginId", "").replace("-", "").strip()
    
    try:
        # 🚨 FIX: Pass 'clean_id' into the encryption function
        encrypted_id = encrypt_abdm_data(clean_id)
    except Exception as e:
        return {"status_code": 500, "data": {"error": f"Encryption failed: {str(e)}"}}
    
    payload = {
        "scope": SCOPE_MAP[data.get("action")], 
        "loginHint": data.get("loginHint"),
        "loginId": encrypted_id,
        "otpSystem": data.get("otpSystem")
    }

    headers = {
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "Authorization": auth_header,
        "X-token": x_token  
    }

    response = requests.post(url=url, json=payload, headers=headers)
    return {"status_code": response.status_code, "data": response.json() if response.ok else response.text}

# =========================================================
# ⚙️ STEP 2: VERIFY OTP OR PASSWORD FOR ANY PROFILE ACTION
# =========================================================
def profile_verify_service(data, auth_header, x_token):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/verify"
    
    try:
        encrypted_auth_value = encrypt_abdm_data(data.get("authValue"))
    except Exception as e:
        return {"status_code": 500, "data": {"error": f"Encryption failed: {str(e)}"}}

    auth_method = data.get("authMethod")

    payload = {
        "scope": SCOPE_MAP[data.get("action")], 
        "authData": {
            "authMethods": [auth_method],
            auth_method: {
                "txnId": data.get("txnId") if auth_method == "otp" else None,
                "otpValue" if auth_method == "otp" else "password": encrypted_auth_value
            }
        }
    }

    # Clean up None values for password flow
    if auth_method == "password":
        del payload["authData"]["password"]["txnId"]

    headers = {
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "Authorization": auth_header,
        "X-token": x_token
    }

    response = requests.post(url=url, json=payload, headers=headers)
    try:
        res_data = response.json()
    except ValueError:
        res_data = {"raw_error": response.text}
        
    return {"status_code": response.status_code, "data": res_data}

# =========================================================
# 📧 DEDICATED STEP: REQUEST EMAIL LINK
# =========================================================
def profile_email_link_service(data, auth_header, x_token):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/request/emailVerificationLink"
    
    try:
        encrypted_email = encrypt_abdm_data(data.get("loginId"))
    except Exception as e:
        return {"status_code": 500, "data": {"error": f"Encryption failed: {str(e)}"}}

    payload = {
        "scope": ["abha-profile", "email-link-verify"],
        "loginHint": "email",
        "loginId": encrypted_email,
        "otpSystem": "abdm",
        "txnId": data.get("txnId")
    }

    headers = {
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "Authorization": auth_header,
        "X-token": x_token
    }

    response = requests.post(url=url, json=payload, headers=headers)
    return {"status_code": response.status_code, "data": response.json() if response.ok else response.text}
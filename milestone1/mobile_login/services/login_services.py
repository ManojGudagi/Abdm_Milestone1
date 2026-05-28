import base64
import uuid
import requests
from django.core.cache import cache
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
# 📱 MOBILE STEP 1: REQUEST OTP
# =========================================================
def send_mobile_otp(data, auth_header):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/request/otp"
    
    try:
        # Backend automatically encrypts the raw mobile number
        encrypted_mobile = encrypt_abdm_data(data.get("mobileNumber"))
    except Exception as e:
        return {"status_code": 500, "data": {"error": f"Encryption failed: {str(e)}"}}

    payload = {
        "scope": ["abha-login", "mobile-verify"], # Hardcoded for mobile flow
        "loginHint": "mobile",
        "loginId": encrypted_mobile,
        "otpSystem": "abdm"
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
# 📱 MOBILE STEP 2: VERIFY OTP (Returns Array of Accounts)
# =========================================================
def verify_mobile_otp(data, auth_header):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify"
    
    try:
        encrypted_otp = encrypt_abdm_data(data.get("otpValue"))
    except Exception as e:
        return {"status_code": 500, "data": {"error": f"Encryption failed: {str(e)}"}}

    payload = {
        "scope": ["abha-login", "mobile-verify"],
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
    
    try:
        res_data = response.json()
    except ValueError:
        res_data = {"raw_error": response.text}
        
    # 🎯 Cache the Temporary Token using the NEW txnId from the response
    if response.ok and "token" in res_data:
        new_txn_id = res_data.get("txnId")
        if new_txn_id:
            cache.set(f"t_token_{new_txn_id}", res_data["token"], timeout=300) # 5 min timeout
        
    return {"status_code": response.status_code, "data": res_data}

# =========================================================
# 📱 MOBILE STEP 3: VERIFY USER (Final Session Token)
# =========================================================
def verify_mobile_user(data, auth_header, t_token):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify/user"
    
    payload = {
        "ABHANumber": data.get("ABHANumber"), # Sent as plain text
        "txnId": data.get("txnId")
    }

    headers = {
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "Authorization": auth_header,
        "T-token": t_token  # 👈 CRITICAL: lowercase 't' as required by ABDM Gateway
    }

    response = requests.post(url=url, json=payload, headers=headers)

    try:
        res_data = response.json()
    except ValueError:
        res_data = {"raw_error": response.text}
        
    return {"status_code": response.status_code, "data": res_data}
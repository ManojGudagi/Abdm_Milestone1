import base64
import requests
import uuid
from datetime import datetime, timezone
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key


def get_abdm_timestamp():

    return datetime.now(
        timezone.utc
    ).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

def encrypt_abdm_data(plaintext: str) -> str:
    """Encrypts plaintext data using ABDM's RSA Public Key"""
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



# =========================================================
# ✅ SEND MOBILE OTP
# =========================================================
def send_mobile_otp(data, auth_header):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/request/otp"

    headers = {
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "Authorization": auth_header
    }

    # 1. Grab raw strings from the frontend data
    txn_id = str(data.get("txnId", "")).strip()
    raw_login_id = str(data.get("loginId", "")).strip()

    # 2. 🛑 FIX: Encrypt the plain mobile number using ABDM's RSA key
    try:
        encrypted_login_id = encrypt_abdm_data(raw_login_id)
    except Exception as e:
        return {
            "status_code": 500,
            "data": {"error": f"Failed to encrypt mobile number: {str(e)}"}
        }

    # 3. Build payload sending the ENCRYPTED string to ABDM
    payload = {
        "txnId": txn_id,
        "scope": ["abha-enrol", "mobile-verify"],
        "loginHint": "mobile",
        "loginId": encrypted_login_id,
        "otpSystem": "abdm"
    }

    print("FINAL HEADERS:", headers)
    # Be careful printing this in production as the encrypted string is massive
    print("FINAL PAYLOAD:", payload)

    response = requests.post(url=url, json=payload, headers=headers)

    try:
        response_data = response.json()
    except Exception:
        response_data = response.text

    print("SEND MOBILE OTP RESPONSE:", response_data)

    return {
        "status_code": response.status_code,
        "data": response_data
    }


# =========================================================
# ✅ VERIFY MOBILE OTP 
# =========================================================
def verify_mobile_otp(data, auth_header):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/auth/byAbdm"

    headers = {
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "Authorization": auth_header
    }

    # 1. Safely extract plain variables using .get()
    raw_txn_id = data.get("txnId")
    raw_otp = data.get("otp") or data.get("otpValue")
    raw_mobile = data.get("mobile", "") 

    # Clean check validation
    if not raw_txn_id or not raw_otp:
        return {
            "status_code": 400,
            "data": {"error": "Missing txnId or otpValue in the request payload"}
        }

    # Ensure extracted fields are clean strings
    txn_id = str(raw_txn_id).strip()
    plain_otp = str(raw_otp).strip()
    mobile = str(raw_mobile).strip()

    # 2. 🛑 FIX: Encrypt the plain OTP before sending to ABDM
    try:
        encrypted_otp = encrypt_abdm_data(plain_otp)
    except Exception as e:
        return {
            "status_code": 500,
            "data": {"error": f"Failed to encrypt OTP: {str(e)}"}
        }

    # 3. Build ABDM Payload with the encrypted OTP
    payload = {
        "scope": [
            "abha-enrol", 
            "mobile-verify"
        ],
        "authData": {
            "authMethods": [
                "otp"
            ],
            "otp": {
                "txnId": txn_id,
                "otpValue": encrypted_otp,  # 👈 ABDM gets the encrypted version!
                "mobile": mobile
            }
        },
        "consent": {
            "code": "abha-enrollment",
            "version": "1.4"
        }
    }

    print("VERIFY MOBILE OTP HEADERS:", headers)
    # Be careful printing the payload in production as it contains the long encrypted string
    print("VERIFY MOBILE OTP PAYLOAD:", payload)

    response = requests.post(url=url, json=payload, headers=headers)

    try:
        response_data = response.json()
    except requests.exceptions.JSONDecodeError:
        response_data = {
            "error": "Non-JSON response received from ABDM gateway during verification.",
            "details": response.text
        }

    print("VERIFY MOBILE OTP RESPONSE:", response_data)

    # 4. Grab the X-Token from the ABDM response headers!
    x_token = response.headers.get("X-Token")

    return {
        "status_code": response.status_code,
        "data": response_data,
        "x_token": x_token
    }
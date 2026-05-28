import base64
import uuid
import requests
from datetime import datetime, timezone
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key

def get_abdm_timestamp():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")

def get_otp_timestamp():
    # DL Verify OTP requires a specific timestamp format: YYYY-MM-DD HH:mm:ss
    return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

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
# 🚗 STEP 1: DL SEND OTP
# =========================================================
def send_dl_otp(data, auth_header):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/request/otp"
    headers = {
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "Authorization": auth_header
    }

    try:
        encrypted_mobile = encrypt_abdm_data(data.get("loginId"))
    except Exception as e:
        return {"status_code": 500, "data": {"error": f"Encryption failed: {str(e)}"}}

    payload = {
        "scope": ["abha-enrol", "mobile-verify", "dl-flow"], # 👈 Unique to DL flow
        "loginHint": "mobile",
        "loginId": encrypted_mobile,
        "otpSystem": "abdm"
    }

    response = requests.post(url=url, json=payload, headers=headers)
    return {"status_code": response.status_code, "data": response.json() if response.ok else response.text}

# =========================================================
# 🚗 STEP 2: DL VERIFY OTP
# =========================================================
def verify_dl_otp(data, auth_header):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/auth/byAbdm"
    headers = {
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "Authorization": auth_header
    }

    try:
        encrypted_otp = encrypt_abdm_data(data.get("otpValue"))
    except Exception as e:
        return {"status_code": 500, "data": {"error": f"Encryption failed: {str(e)}"}}

    payload = {
        "scope": ["abha-enrol", "mobile-verify", "dl-flow"],
        "authData": {
            "authMethods": ["otp"],
            "otp": {
                "timeStamp": get_otp_timestamp(), # 👈 ABDM uniquely requires this here
                "txnId": data.get("txnId"),
                "otpValue": encrypted_otp
            }
        }
    }

    response = requests.post(url=url, json=payload, headers=headers)
    return {"status_code": response.status_code, "data": response.json() if response.ok else response.text}

# =========================================================
# 🚗 STEP 3: SUBMIT DL DOCUMENT
# =========================================================
def verify_dl_document(data, auth_header):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/byDocument"
    headers = {
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "Authorization": auth_header
    }

    # Pass the plain data straight through (No RSA encryption for these fields!)
    payload = {
        "txnId": data.get("txnId"),
        "documentType": "DRIVING_LICENCE",
        "documentId": data.get("documentId"),
        "firstName": data.get("firstName"),
        "middleName": data.get("middleName"),
        "lastName": data.get("lastName"),
        "dob": data.get("dob"),
        "gender": data.get("gender"),
        "frontSidePhoto": data.get("frontSidePhoto"),
        "backSidePhoto": data.get("backSidePhoto"),
        "address": data.get("address"),
        "state": data.get("state"),
        "district": data.get("district"),
        "pinCode": data.get("pinCode"),
        "consent": {
            "code": "abha-enrollment",
            "version": "1.4"
        }
    }

    response = requests.post(url=url, json=payload, headers=headers)
    return {"status_code": response.status_code, "data": response.json() if response.ok else response.text}
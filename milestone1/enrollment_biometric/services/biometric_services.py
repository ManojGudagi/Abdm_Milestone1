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
# 📸 STEP 1: INIT FACE AUTH
# =========================================================
def init_face_auth(auth_header):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/auth/init"
    headers = {
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "Authorization": auth_header
    }
    payload = {"scope": ["abha-enrol", "face-auth"]}
    
    response = requests.post(url=url, json=payload, headers=headers)
    return {"status_code": response.status_code, "data": response.json() if response.ok else response.text}

# =========================================================
# 📸 STEP 2: CHECK FACE AUTH STATUS
# =========================================================
def check_face_auth_status(txn_id, auth_header):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/capturePID"
    headers = {
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "Authorization": auth_header
    }
    payload = {
        "scope": ["abha-enrol", "face-verify"],
        "txnId": str(txn_id)
    }
    
    response = requests.post(url=url, json=payload, headers=headers)
    return {"status_code": response.status_code, "data": response.json() if response.ok else response.text}

# =========================================================
# 👆 👁️ 📸 STEP 3: UNIFIED BIOMETRIC ENROLLMENT
# =========================================================
def enrol_via_biometric(data, auth_header):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/byAadhaar"
    headers = {
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "Authorization": auth_header
    }

    # 1. Encrypt the plain ID on the backend securely
    try:
        encrypted_id = encrypt_abdm_data(data.get("aadhaarNumber"))
    except Exception as e:
        return {"status_code": 500, "data": {"error": f"Encryption failed: {str(e)}"}}

    # 2. Build the base payload
    auth_method = data.get("authMethod")
    payload = {
        "authData": {
            "authMethods": [auth_method],
            # We will dynamically inject the specific dictionary below
        },
        "consent": {
            "code": "abha-enrollment",
            "version": "1.4"
        }
    }

    # 3. Inject the correct sub-dictionary based on the chosen method
    if auth_method == "bio":
        payload["authData"]["bio"] = {
            "aadhaar": encrypted_id,
            "fingerPrintAuthPid": data.get("pid", ""),
            "mobile": data.get("mobile", "")
        }
    elif auth_method == "iris":
        payload["authData"]["iris"] = {
            "aadhaar": encrypted_id,
            "pid": data.get("pid", ""),
            "mobile": data.get("mobile", "")
        }
    elif auth_method == "face_auth":
        payload["authData"]["face"] = {
            "txnId": data.get("txnId"),
            "aadhaar": encrypted_id,
            "mobile": data.get("mobile", "")
        }

    response = requests.post(url=url, json=payload, headers=headers)
    
    try:
        response_data = response.json()
    except ValueError:
        response_data = {"raw_error": response.text}
        
    return {"status_code": response.status_code, "data": response_data}
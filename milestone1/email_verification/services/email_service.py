import base64
import requests
import uuid
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key

# Make sure to import your get_abdm_timestamp function!
from milestone1.enrollment_aadhaar.views.otp_view import get_abdm_timestamp

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

def send_email_verification(email: str, auth_header: str, x_token: str):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/request/emailVerificationLink"

    headers = {
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "Authorization": auth_header,
        "X-token": f"Bearer {x_token}"  
    }

    encrypted_email = encrypt_abdm_data(email)

    payload = {
        "scope": [
            "abha-profile",
            "email-link-verify"
        ],
        "loginHint": "email",
        "loginId": encrypted_email,
        "otpSystem": "abdm"
    }

    response = requests.post(url=url, json=payload, headers=headers)

    # ✅ Handle the empty response body specifically for this endpoint
    if response.status_code == 200:
        return {
            "status_code": 200,
            "data": {"message": "Email verification link sent successfully."}
        }
    
    # If it failed, try to read the JSON error
    try:
        response_data = response.json()
    except requests.exceptions.JSONDecodeError:
        response_data = {"error": "Failed to send email verification", "details": response.text}

    return {
        "status_code": response.status_code,
        "data": response_data
    }
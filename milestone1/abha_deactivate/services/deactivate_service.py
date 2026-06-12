import uuid
import requests

# ✅ Looking locally for your copied utils.py
from ..utils import (
    get_abdm_timestamp, 
    encrypt_abdm_data, 
    get_abdm_access_token 
)

def generate_deactivate_otp_service(plaintext_abha: str, x_token: str, gateway_token: str) -> tuple[dict, int]:
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/request/otp"
    
    try:
        encrypted_abha = encrypt_abdm_data(plaintext_abha)
    except Exception as e:
        return {"error": f"Encryption failed: {str(e)}"}, 500

    access_token = get_abdm_access_token()

    if not x_token.startswith("Bearer "):
        x_token = f"Bearer {x_token}"

    headers = {
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "Authorization": f"Bearer {access_token}",
        "X-token": x_token 
    }

    payload = {
        "scope": ["abha-profile", "de-activate"], # ✅ Updated Scope
        "loginHint": "abha-number",
        "loginId": encrypted_abha,
        "otpSystem": "aadhaar"
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        return res.json(), res.status_code
    except requests.exceptions.RequestException as e:
        return {"error": "Failed to connect to ABDM", "details": str(e)}, 503


def verify_deactivate_otp_service(txn_id: str, plaintext_otp: str, reasons: str, x_token: str, gateway_token: str) -> tuple[dict, int]:
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/verify"
    
    try:
        encrypted_otp = encrypt_abdm_data(plaintext_otp)
    except Exception as e:
        return {"error": f"Encryption failed: {str(e)}"}, 500

    access_token = get_abdm_access_token()

    if not x_token.startswith("Bearer "):
        x_token = f"Bearer {x_token}"

    headers = {
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "Authorization": f"Bearer {access_token}",
        "X-token": x_token
    }

    payload = {
        "scope": ["abha-profile", "de-activate"], # ✅ Updated Scope
        "authData": {
            "authMethods": ["otp"],
            "otp": {
                "txnId": txn_id,
                "otpValue": encrypted_otp
            }
        },
        "reasons": reasons # ✅ Appended reasons array
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        return res.json(), res.status_code
    except requests.exceptions.RequestException as e:
        return {"error": "Failed to connect to ABDM", "details": str(e)}, 503
import uuid
import requests
from django.conf import settings

# ✅ Point directly to the new local utils file we just created
from milestone1.abhanumber_recover.utils import (
    get_abdm_timestamp, 
    encrypt_abdm_data, 
    get_abdm_access_token 
)

def generate_recovery_otp_service(login_hint: str, plaintext_id: str) -> tuple[dict, int]:
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/request/otp"
    
    try:
        encrypted_id = encrypt_abdm_data(plaintext_id)
    except Exception as e:
        return {"error": f"Encryption failed: {str(e)}"}, 500

    access_token = get_abdm_access_token()

    headers = {
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "Authorization": f"Bearer {access_token}"
    }

    # ✅ Dynamically set the payload based on the "clue"
    if login_hint == "aadhaar":
        payload = {
            "scope": ["abha-login", "aadhaar-verify"],
            "loginHint": "aadhaar",
            "loginId": encrypted_id,
            "otpSystem": "aadhaar"
        }
    else: # mobile
        payload = {
            "scope": ["abha-login", "mobile-verify"],
            "loginHint": "mobile",
            "loginId": encrypted_id,
            "otpSystem": "abdm"
        }

    try:
        res = requests.post(url, headers=headers, json=payload)
        return res.json(), res.status_code
    except requests.exceptions.RequestException as e:
        return {"error": "Failed to connect to ABDM", "details": str(e)}, 503


def verify_recovery_otp_service(login_hint: str, txn_id: str, plaintext_otp: str) -> tuple[dict, int]:
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/profile/login/verify"
    
    try:
        encrypted_otp = encrypt_abdm_data(plaintext_otp)
    except Exception as e:
        return {"error": f"Encryption failed: {str(e)}"}, 500

    access_token = get_abdm_access_token()

    headers = {
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "Authorization": f"Bearer {access_token}"
    }

    # ✅ Dynamically set the correct scope
    scope = ["abha-login", "aadhaar-verify"] if login_hint == "aadhaar" else ["abha-login", "mobile-verify"]

    payload = {
        "scope": scope,
        "authData": {
            "authMethods": ["otp"],
            "otp": {
                "txnId": txn_id,
                "otpValue": encrypted_otp
            }
        }
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        return res.json(), res.status_code
    except requests.exceptions.RequestException as e:
        return {"error": "Failed to connect to ABDM", "details": str(e)}, 503
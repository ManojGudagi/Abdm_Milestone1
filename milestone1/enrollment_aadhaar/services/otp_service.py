# milestone1/enrollment_aadhaar/services/otp_service.py

import uuid
import random
from datetime import datetime, timedelta

from django.utils.timezone import now

from milestone1.enrollment_aadhaar.models import OTPTransaction
from milestone1.enrollment_aadhaar.services.encryption_service import decrypt_data  # ✅ updated

OTP_EXPIRY_SECONDS = 300
MAX_ATTEMPTS = 3


def generate_txn_id():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{uuid.uuid4()}:{timestamp}"


def mask_mobile():
    return "xxx001"  # TODO: map from Aadhaar


# 🚀 GENERATE OTP
def generate_otp(data, client_id):
    txn_id = data.get("txnId") or generate_txn_id()

    encoded_aadhaar = data.get("loginId")

    # ✅ Decode Base64 Aadhaar
    try:
        aadhaar_number = decrypt_data(encoded_aadhaar)
    except Exception:
        return {"error": "Invalid encoded Aadhaar"}

    # ✅ Validate Aadhaar format
    if len(aadhaar_number) != 12 or not aadhaar_number.isdigit():
        return {"error": "Invalid Aadhaar format"}

    # 🔐 (Optional) log or use aadhaar_number internally
    # print("Decoded Aadhaar:", aadhaar_number)

    otp = str(random.randint(1000, 9999))

    # If same txn_id reused, overwrite safely
    OTPTransaction.objects.update_or_create(
        txn_id=txn_id,
        defaults={
            "otp": otp,
            "client_id": client_id,
            "is_verified": False,
            "attempts": 0,
            "expires_at": now() + timedelta(seconds=OTP_EXPIRY_SECONDS),
        },
    )

    return {
        "txnId": txn_id,
        "message": f"OTP is sent to Aadhaar registered mobile ending {mask_mobile()}",
        # "debugOtp": otp  # enable only for testing
    }


# 🚀 VERIFY OTP (no change needed)
def verify_otp(txn_id, encoded_otp, client_id):
    try:
        record = OTPTransaction.objects.get(txn_id=txn_id)
    except OTPTransaction.DoesNotExist:
        return {"status": False, "message": "Invalid txnId"}

    # 🔓 Decode OTP
    try:
        otp = decrypt_data(encoded_otp)
    except Exception:
        return {"status": False, "message": "Invalid OTP format"}

    # Already used
    if record.is_verified:
        return {"status": False, "message": "OTP already used"}

    # Client check
    if record.client_id != client_id:
        return {"status": False, "message": "Unauthorized txn access"}

    # Expiry
    if record.is_expired():
        return {"status": False, "message": "OTP expired"}

    # Attempts limit
    if record.attempts >= MAX_ATTEMPTS:
        return {"status": False, "message": "Max attempts exceeded"}

    # ❌ Wrong OTP
    if record.otp != str(otp):
        record.attempts += 1
        record.save(update_fields=["attempts"])
        return {
            "status": False,
            "message": "Invalid OTP",
            "remainingAttempts": MAX_ATTEMPTS - record.attempts,
        }

    # ✅ SUCCESS
    record.is_verified = True
    record.save(update_fields=["is_verified"])

    return {
        "status": True,
        "message": "OTP verified successfully",
    }
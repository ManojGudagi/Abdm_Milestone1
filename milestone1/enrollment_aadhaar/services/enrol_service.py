import base64
from datetime import datetime

from milestone1.enrollment_aadhaar.services.otp_service import verify_otp
from milestone1.enrollment_aadhaar.services.jwt_service import generate_access_token, generate_refresh_token



import base64

def decode_base64(data):
    decoded = base64.b64decode(data).decode("utf-8")

        # ✅ Ensure OTP is numeric and 4 digits
    if not decoded.isdigit() or len(decoded) != 4:
            raise Exception("Invalid OTP format")
    print("DECODED OTP:", decoded)
    return decoded


# def enrol_abha(data, client_id):
    try:
        otp_data = data["authData"]["otp"]

        txn_id = otp_data["txnId"]
        encoded_otp = otp_data["otpValue"]

        # ✅ Decode OTP
        otp = decode_base64(encoded_otp)

        # ✅ Verify OTP
        result = verify_otp(txn_id, otp, client_id)

        if not result["status"]:
            return result

        # ✅ Generate ABHA mock response
        access_token = generate_access_token(client_id)
        refresh_token = generate_refresh_token(client_id)

        return {
            "message": "Account created successfully",
            "txnId": txn_id,
            "tokens": {
                "token": access_token,
                "expiresIn": 1800,
                "refreshToken": refresh_token,
                "refreshExpiresIn": 1296000
            },
            "ABHAProfile": {
                "firstName": "Test",
                "lastName": "User",
                "dob": "01-01-1990",
                "mobile": "******001",
                "gender": "M",
                "ABHANumber": "91-XXXX-XXXX",
                "abhaStatus": "ACTIVE"
            },
            "isNew": True
        }

    except Exception as e:
        return {
            "status": False,
            "message": str(e)
        }
def enrol_abha(data, client_id):
    try:
        otp_data = data["authData"]["otp"]

        txn_id = otp_data["txnId"]
        encoded_otp = otp_data["otpValue"]
        mobile = otp_data["mobile"]

        # Decode OTP
        otp = decode_base64(encoded_otp)

        # Verify OTP
        result = verify_otp(txn_id, otp, client_id)

        if not result["status"]:
            return result

        # Generate tokens
        access_token = generate_access_token(client_id)
        refresh_token = generate_refresh_token(client_id)

        # Dynamic response in same structure
        return {
            "message": "Account created successfully",
            "txnId": txn_id,
            "tokens": {
                "token": access_token,
                "expiresIn": 1800,
                "refreshToken": refresh_token,
                "refreshExpiresIn": 1296000
            },
            "ABHAProfile": {
                "firstName": result.get("firstName", ""),
                "middleName": result.get("middleName", ""),
                "lastName": result.get("lastName", ""),
                "dob": result.get("dob", ""),
                "gender": result.get("gender", ""),
                "photo": result.get("photo", ""),
                "mobile": mobile[:2] + "******" + mobile[-2:],
                "phrAddress": result.get("phrAddress", []),
                "address": result.get("address", ""),
                "districtCode": result.get("districtCode", ""),
                "stateCode": result.get("stateCode", ""),
                "pinCode": result.get("pinCode", ""),
                "abhaType": result.get("abhaType", "STANDARD"),
                "stateName": result.get("stateName", ""),
                "districtName": result.get("districtName", ""),
                "ABHANumber": result.get("ABHANumber", ""),
                "abhaStatus": result.get("abhaStatus", "ACTIVE")
            },
            "isNew": True
        }

    except Exception as e:
        return {
            "status": False,
            "message": str(e)
        }
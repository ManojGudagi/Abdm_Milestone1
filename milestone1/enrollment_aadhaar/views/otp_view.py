# milestone1/enrollment_aadhaar/views/otp_view.py
import base64
import uuid
import requests
import hashlib
from datetime import datetime, timezone
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key

from milestone1.enrollment_aadhaar.serializers.otp_serializer import (
    AadhaarOtpRequestSerializer,
    AadhaarOTPVerifySerializer,
    SendOtpSerializer
)
from milestone1.enrollment_aadhaar.services.otp_service import generate_otp, verify_otp
from milestone1.enrollment_aadhaar.services.jwt_service import verify_token


# -----------------------------------------------------------------------------
# 🔐 Common Auth & Helpers
# -----------------------------------------------------------------------------

def get_abdm_timestamp():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def validate_auth_header(request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None, Response({"error": "Authorization header missing"}, status=401)

    if not auth_header.startswith("Bearer "):
        return None, Response({"error": "Invalid token format"}, status=401)

    token = auth_header.split(" ")
    decoded = verify_token(token)

    if not decoded:
        return None, Response({"error": "Invalid or expired token"}, status=401)

    return decoded, None


# -----------------------------------------------------------------------------
# 🚀 SEND OTP (Standard)
# -----------------------------------------------------------------------------

class AadhaarOtpView(APIView):
    def post(self, request):
        # ✅ Header validation
        request_id = request.headers.get("REQUEST-ID")
        timestamp = request.headers.get("TIMESTAMP")

        if not request_id or not timestamp:
            return Response(
                {"error": "Missing required headers"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Token validation
        decoded, error = validate_auth_header(request)
        if error:
            return error
        client_id = decoded.get("sub")
        
        # ✅ Body validation
        serializer = AadhaarOtpRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        response = generate_otp(serializer.validated_data, client_id)

        return Response(response, status=200)


# -----------------------------------------------------------------------------
# 🚀 VERIFY OTP (Nested ABDM Format)
# -----------------------------------------------------------------------------

class AadhaarOtpVerifyView(APIView):
    @swagger_auto_schema(
        operation_summary="Verify OTP",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "txnId": openapi.Schema(type=openapi.TYPE_STRING, description="Transaction ID from send OTP response"),
                "otpValue": openapi.Schema(type=openapi.TYPE_STRING, description="Plaintext OTP entered by user"),
                "mobile": openapi.Schema(type=openapi.TYPE_STRING, default="", description="Optional mobile number"),
            },
            example={
                "txnId": "",
                "otpValue": "",
                "mobile": ""
            }
        ),
        responses={200: "OTP Verified"}
    )
    def post(self, request):
        # ⚠️ Update this URL to the exact ABDM v3 verification endpoint you are using 
        # (e.g., /enrol/byAadhaar or /auth/byAbha depending on your flow)
        abdm_verify_url = "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/byAadhaar"

        # 1. Validate Auth Header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return Response({"error": "Authorization header missing"}, status=401)

        # 2. Extract plaintext data from frontend request
        txn_id = request.data.get("txnId")
        plaintext_otp = request.data.get("otpValue")
        mobile = request.data.get("mobile", "")

        if not txn_id or not plaintext_otp:
            return Response(
                {"error": "txnId and otpValue are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Encrypt the plaintext OTP using ABDM's RSA public key
        try:
            encrypted_otp = self.encrypt_abdm_data(plaintext_otp)
        except Exception as e:
            return Response({"error": f"Encryption failed: {str(e)}"}, status=500)

        # 4. Construct the nested payload required by ABDM
        abdm_payload = {
            "authData": {
                "authMethods": ["otp"],
                "otp": {
                    "txnId": txn_id,
                    "otpValue": encrypted_otp,
                    "mobile": mobile
                }
            },
            "consent": {
                "code": "abha-enrollment",
                "version": "1.4"
            }
        }

        # 5. Set up headers for the ABDM request
        headers = {
            "Content-Type": "application/json",
            "REQUEST-ID": str(uuid.uuid4()),
            "TIMESTAMP": get_abdm_timestamp(),
            "Authorization": auth_header
        }

        # 6. Send the request to ABDM
        res = requests.post(abdm_verify_url, headers=headers, json=abdm_payload)

        # 7. Safely parse the JSON response
        try:
            response_data = res.json()
        except requests.exceptions.JSONDecodeError:
            return Response(
                {"error": "Invalid JSON response from ABDM", "details": res.text}, 
                status=res.status_code
            )

        # 8. ✅ X-TOKEN EXTRACTION & CACHING LOGIC
        # First, try to get it from the Header (New Account Scenario)
        x_token = res.headers.get("X-Token")

        # If it's not in the header, try to get it from the JSON Body (Existing Account Scenario)
        if not x_token and isinstance(response_data, dict):
            tokens_dict = response_data.get("tokens", {})
            x_token = tokens_dict.get("token")

        # If we successfully found a token, save it to the Django cache!
        if x_token:
            raw_token = auth_header.replace("Bearer ", "").strip()
            token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
            cache.set(f"x_token_{token_hash}", x_token, timeout=1800)
            print("✅ Successfully cached new X-Token from Aadhaar Verify!")

        # 9. Return the data to the frontend
        return Response(response_data, status=res.status_code)

    def encrypt_abdm_data(self, plaintext: str) -> str:
        """
        Encrypts data using RSA/ECB/OAEPWithSHA-1AndMGF1Padding
        """
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


# -----------------------------------------------------------------------------
# 🚀 SEND OTP (Encrypted ABDM Request)
# -----------------------------------------------------------------------------

class SendOtpView(APIView):
    @swagger_auto_schema(
        operation_summary="Send OTP",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "txnId": openapi.Schema(type=openapi.TYPE_STRING, default=""),
                "scope": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                    default=["abha-enrol"]
                ),
                "loginHint": openapi.Schema(type=openapi.TYPE_STRING, default="aadhaar"),
                "loginId": openapi.Schema(type=openapi.TYPE_STRING, default=""),
                "otpSystem": openapi.Schema(type=openapi.TYPE_STRING, default="aadhaar"),
            },
            example={
                "txnId": "",
                "scope": [
                    "abha-enrol"
                ],
                "loginHint": "aadhaar",
                "loginId": "", 
                "otpSystem": "aadhaar"
            }
        )
    )
    def post(self, request):
        url = "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/request/otp"

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return Response({"error": "Authorization header missing"}, status=401)

        # 1. Grab the plaintext number from the frontend request
        plaintext_login_id = request.data.get("loginId", "")

        # 2. Encrypt it internally using ABDM's requested RSA algorithm
        try:
            encrypted_login_id = self.encrypt_abdm_data(plaintext_login_id)
        except Exception as e:
            return Response({"error": f"Encryption failed: {str(e)}"}, status=500)

        headers = {
            "Content-Type": "application/json",
            "REQUEST-ID": str(uuid.uuid4()),
            "TIMESTAMP": get_abdm_timestamp(),
            "Authorization": auth_header
        }

        # 3. Construct payload sending the ENCRYPTED string to ABDM
        payload = {
            "txnId": request.data.get("txnId", ""),
            "scope": request.data.get("scope", ["abha-enrol"]),
            "loginHint": request.data.get("loginHint", "aadhaar"),
            "loginId": encrypted_login_id,
            "otpSystem": request.data.get("otpSystem", "aadhaar")
        }

        res = requests.post(url, headers=headers, json=payload)
        
        # Safely handle the response in case ABDM doesn't return JSON
        try:
            return Response(res.json(), status=res.status_code)
        except requests.exceptions.JSONDecodeError:
            return Response({"error": "Invalid JSON response from ABDM", "details": res.text}, status=res.status_code)

    def encrypt_abdm_data(self, plaintext: str) -> str:
        """
        Encrypts data using RSA/ECB/OAEPWithSHA-1AndMGF1Padding (Legacy)
        """
        if not plaintext:
            return ""

        # DO NOT indent the BEGIN or END lines. They must be flush left.
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
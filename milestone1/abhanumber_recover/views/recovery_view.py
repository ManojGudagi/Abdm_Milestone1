from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from milestone1.abhanumber_recover.serializers.recovery_serializer import (
    GenerateRecoveryOtpSerializer,
    VerifyRecoveryOtpSerializer
)
from milestone1.abhanumber_recover.services.recovery_service import (
    generate_recovery_otp_service,
    verify_recovery_otp_service
)
from milestone1.enrollment_aadhaar.services.jwt_service import verify_token

def validate_client_token(request):
    """Local helper to validate your frontend's JWT."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None, Response({"error": "Invalid or missing Authorization header"}, status=401)
    
    token = auth_header.split(" ")
    decoded = verify_token(token)
    if not decoded:
        return None, Response({"error": "Invalid or expired token"}, status=401)
    return decoded, None


class GenerateRecoveryOtpView(APIView):
    @swagger_auto_schema(
        operation_summary="Forgot ABHA: Generate OTP",
        request_body=GenerateRecoveryOtpSerializer,
        responses={200: "OTP Sent"}
    )
    def post(self, request):
        # decoded, error = validate_client_token(request)
        # if error: return error

        serializer = GenerateRecoveryOtpSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        # ✅ Extract both values
        login_hint = serializer.validated_data["loginHint"]
        plaintext_id = serializer.validated_data["loginId"]
        
        # ✅ Pass both values to the service
        response_data, status_code = generate_recovery_otp_service(login_hint, plaintext_id)

        return Response(response_data, status=status_code)


class VerifyRecoveryOtpView(APIView):
    @swagger_auto_schema(
        operation_summary="Forgot ABHA: Verify OTP",
        request_body=VerifyRecoveryOtpSerializer,
        responses={200: "OTP Verified, T-Token returned"}
    )
    def post(self, request):
        # decoded, error = validate_client_token(request)
        # if error: return error

        serializer = VerifyRecoveryOtpSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        # ✅ Extract the hint, txn_id, and otp
        login_hint = serializer.validated_data["loginHint"]
        txn_id = serializer.validated_data["txnId"]
        plaintext_otp = serializer.validated_data["otpValue"]
        
        # ✅ Pass them all to the service
        response_data, status_code = verify_recovery_otp_service(login_hint, txn_id, plaintext_otp)

        return Response(response_data, status=status_code)

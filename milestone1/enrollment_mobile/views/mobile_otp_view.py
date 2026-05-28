from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import hashlib
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi  # 👈 Added to construct manual schemas

from milestone1.enrollment_mobile.serializers.mobile_otp_serializer import (
    MobileOtpRequestSerializer,
    MobileOtpVerifySerializer
)

from milestone1.enrollment_mobile.services.mobile_otp_service import (
    send_mobile_otp,
    verify_mobile_otp
)


# =========================================================
# ✅ SEND MOBILE OTP VIEW
# =========================================================
class SendMobileOtpView(APIView):
    # Bypass DRF global auth if gateway tokens are being handled manually
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="Send Mobile OTP",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['txnId', 'loginId'],
            properties={
                "txnId": openapi.Schema(type=openapi.TYPE_STRING, description="Transaction ID from initial validation response"),
                "loginId": openapi.Schema(type=openapi.TYPE_STRING, description="The mobile number to register or verify"),
            },
            example={
                "txnId": "123e4567-e89b-12d3-a456-426614174000",
                "loginId": "9876543210"
            }
        ),
        responses={200: "OTP Sent successfully"}
    )
    def post(self, request):
        try:
            # ✅ AUTHORIZATION HEADER
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return Response(
                    {"error": "Authorization header missing"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # ✅ VALIDATE BODY
            serializer = MobileOtpRequestSerializer(data=request.data)

            if not serializer.is_valid():
                print(serializer.errors)
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            payload = serializer.validated_data

            # ✅ CALL SERVICE
            result = send_mobile_otp(payload, auth_header)

            print("ABDM RESPONSE:", result)

            return Response(
                result["data"],
                status=result["status_code"]
            )

        except Exception as e:
            import traceback
            traceback.print_exc()  # Prints the real exception traceback locally to terminal
            return Response(
                {
                    "status": False,
                    "message": "Internal server error",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =========================================================
# ✅ VERIFY MOBILE OTP VIEW
# =========================================================
class VerifyMobileOtpView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="Verify Mobile OTP",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['txnId', 'otpValue'],
            properties={
                "txnId": openapi.Schema(type=openapi.TYPE_STRING, description="Transaction ID from send-otp tracking"),
                "otpValue": openapi.Schema(type=openapi.TYPE_STRING, description="The 6-digit verification code received"),
                "mobile": openapi.Schema(type=openapi.TYPE_STRING, description="Optional registered mobile string", default="")
            },
            example={
                "txnId": "123e4567-e89b-12d3-a456-426614174000",
                "otpValue": "123456",
                "mobile": "9876543210"
            }
        ),
        responses={200: "OTP Verified successfully"}
    )
    def post(self, request):
        try:
            # ✅ AUTHORIZATION HEADER
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return Response(
                    {"error": "Authorization header missing"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # ✅ VALIDATE BODY
            serializer = MobileOtpVerifySerializer(data=request.data)

            if not serializer.is_valid():
                print(serializer.errors)
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            payload = serializer.validated_data

            # ✅ CALL SERVICE
            result = verify_mobile_otp(payload, auth_header)

            print("ABDM RESPONSE:", result)

            x_token = result.get("x_token")
            if x_token:
                # Hash the Bearer token to use as a safe cache key
                raw_token = auth_header.replace("Bearer ", "").strip()
                token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
                
                # Save the X-Token to Django's cache
                cache.set(f"x_token_{token_hash}", x_token, timeout=1800)
                print("✅ Successfully cached new X-Token from Mobile Verify!")

            return Response(
                result["data"],
                status=result["status_code"]
            )

        except Exception as e:
            import traceback
            traceback.print_exc()  # Ensures any hidden failures dump trace out cleanly to your logs
            return Response(
                {
                    "status": False,
                    "message": "Internal server error",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
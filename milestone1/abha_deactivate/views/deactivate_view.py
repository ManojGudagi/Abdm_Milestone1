from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..utils import get_user_x_token 

from ..serializers.deactivate_serializer import (
    GenerateDeactivateOtpSerializer,
    VerifyDeactivateOtpSerializer
)
from ..services.deactivate_service import (
    generate_deactivate_otp_service,
    verify_deactivate_otp_service
)

x_token_header = openapi.Parameter(
    'X-Token', 
    openapi.IN_HEADER, 
    description="Paste your X-Token here (Format: 'Bearer <token>')", 
    type=openapi.TYPE_STRING,
    required=False
)

class GenerateDeactivateOtpView(APIView):
    @swagger_auto_schema(
        operation_summary="Deactivate ABHA: Generate OTP",
        request_body=GenerateDeactivateOtpSerializer,
        manual_parameters=[x_token_header],
        responses={200: "OTP Sent"}
    )
    def post(self, request):
        # HYBRID CHECK
        x_token = request.headers.get("X-Token") or get_user_x_token()
        if not x_token:
            return Response({"error": "X-Token missing. Paste it in the Header or run login again."}, status=401)

        serializer = GenerateDeactivateOtpSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
            
        plaintext_abha = serializer.validated_data["ABHANumber"]
        response_data, status_code = generate_deactivate_otp_service(plaintext_abha, x_token)

        return Response(response_data, status=status_code)


class VerifyDeactivateOtpView(APIView):
    @swagger_auto_schema(
        operation_summary="Deactivate ABHA: Verify OTP",
        request_body=VerifyDeactivateOtpSerializer,
        manual_parameters=[x_token_header],
        responses={200: "Account Deactivated"}
    )
    def post(self, request):
        # HYBRID CHECK
        x_token = request.headers.get("X-Token") or get_user_x_token()
        if not x_token:
            return Response({"error": "X-Token missing. Paste it in the Header or run login again."}, status=401)

        serializer = VerifyDeactivateOtpSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        txn_id = serializer.validated_data["txnId"]
        plaintext_otp = serializer.validated_data["otpValue"]
        reasons = serializer.validated_data["reasons"] # ✅ Extract reasons

        # Pass all data to the service
        response_data, status_code = verify_deactivate_otp_service(txn_id, plaintext_otp, reasons, x_token)

        return Response(response_data, status=status_code)
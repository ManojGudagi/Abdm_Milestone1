from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..utils import get_user_x_token 

from ..serializers.delete_serializer import (
    GenerateDeleteOtpSerializer,
    VerifyDeleteOtpSerializer
)
from ..services.delete_service import (
    generate_delete_otp_service,
    verify_delete_otp_service
)

# ✅ Added the Swagger manual parameter back so you can bypass the broken cache
x_token_header = openapi.Parameter(
    'X-Token', 
    openapi.IN_HEADER, 
    description="Paste your X-Token here (Format: 'Bearer <token>')", 
    type=openapi.TYPE_STRING,
    required=False
)

class GenerateDeleteOtpView(APIView):
    @swagger_auto_schema(
        operation_summary="Delete ABHA: Generate OTP",
        request_body=GenerateDeleteOtpSerializer,
        manual_parameters=[x_token_header],
        responses={200: "OTP Sent"}
    )
    def post(self, request):
        # 1. HYBRID CHECK: Look at the Header first, then check the Cache
        x_token = request.headers.get("X-Token") or get_user_x_token()
        
        if not x_token:
            return Response({
                "error": "X-Token missing. Please paste it into the Header box or run login again."
            }, status=401)

        # 2. Validate Body
        serializer = GenerateDeleteOtpSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
            
        plaintext_abha = serializer.validated_data["ABHANumber"]

        # 3. Call Service
        response_data, status_code = generate_delete_otp_service(plaintext_abha, x_token)

        return Response(response_data, status=status_code)


class VerifyDeleteOtpView(APIView):
    @swagger_auto_schema(
        operation_summary="Delete ABHA: Verify OTP",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "txnId": openapi.Schema(type=openapi.TYPE_STRING),
                "otpValue": openapi.Schema(type=openapi.TYPE_STRING, description="Plaintext OTP"),
            },
            example={
                "txnId": "{{txnId from step 1}}",
                "otpValue": "123456"
            }
        ),
        manual_parameters=[x_token_header],
        responses={200: "Account Deleted"}
    )
    def post(self, request):
        # 1. HYBRID CHECK: Look at the Header first, then check the Cache
        x_token = request.headers.get("X-Token") or get_user_x_token()
        
        if not x_token:
            return Response({
                "error": "X-Token missing. Please paste it into the Header box or run login again."
            }, status=401)

        # 2. Validate Body
        serializer = VerifyDeleteOtpSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        txn_id = serializer.validated_data["txnId"]
        plaintext_otp = serializer.validated_data["otpValue"]

        # 3. Call Service
        response_data, status_code = verify_delete_otp_service(txn_id, plaintext_otp, x_token)

        return Response(response_data, status=status_code)
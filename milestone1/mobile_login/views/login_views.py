from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.core.cache import cache

from milestone1.mobile_login.serializers.login_serializers import (
    MobileRequestOtpSerializer,
    MobileVerifyOtpSerializer,
    MobileVerifyUserSerializer
)
from milestone1.mobile_login.services.login_services import (
    send_mobile_otp,
    verify_mobile_otp,
    verify_mobile_user
)



# Import your new serializers and services here...

class MobileRequestOtpView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(operation_summary="Mobile Login Step 1: Request OTP", security=[{'Bearer': []}], request_body=MobileRequestOtpSerializer)
    def post(self, request):
        auth = request.headers.get("Authorization")
        serializer = MobileRequestOtpSerializer(data=request.data)
        if serializer.is_valid():
            result = send_mobile_otp(serializer.validated_data, auth)
            return Response(result["data"], status=result["status_code"])
        return Response(serializer.errors, status=400)

class MobileVerifyOtpView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(operation_summary="Mobile Login Step 2: Verify OTP", security=[{'Bearer': []}], request_body=MobileVerifyOtpSerializer)
    def post(self, request):
        auth = request.headers.get("Authorization")
        serializer = MobileVerifyOtpSerializer(data=request.data)
        if serializer.is_valid():
            result = verify_mobile_otp(serializer.validated_data, auth)
            return Response(result["data"], status=result["status_code"])
        return Response(serializer.errors, status=400)

class MobileVerifyUserView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(operation_summary="Mobile Login Step 3: Verify Specific User", security=[{'Bearer': []}], request_body=MobileVerifyUserSerializer)
    def post(self, request):
        auth = request.headers.get("Authorization")
        serializer = MobileVerifyUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
            
        # 1. Look in the cache for the T-Token using the new txnId
        txn_id = serializer.validated_data.get("txnId")
        raw_t_token = cache.get(f"t_token_{txn_id}")
        
        if not raw_t_token:
            return Response({"error": "T-Token missing or expired. Run Step 2 again."}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Aggressive Cleaning: Prevent 'Double Bearer' formatting errors
        clean_token = raw_t_token.strip()
        if clean_token.startswith("Bearer "):
            clean_token = clean_token.replace("Bearer ", "").strip()
            
        formatted_t_token = f"Bearer {clean_token}"

        # 3. Fire the final service
        result = verify_mobile_user(serializer.validated_data, auth, formatted_t_token)
        return Response(result["data"], status=result["status_code"])
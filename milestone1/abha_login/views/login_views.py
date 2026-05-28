from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.core.cache import cache

from milestone1.abha_login.serializers.login_serializers import (
    LoginRequestOtpSerializer, 
    LoginVerifyOtpSerializer
)
from milestone1.abha_login.services.login_services import (
    send_login_otp, 
    verify_login_otp
)

class LoginRequestOtpView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="Login Step 1: Request OTP",
        security=[{'Bearer': []}],
        request_body=LoginRequestOtpSerializer
    )
    def post(self, request):
        auth = request.headers.get("Authorization")
        serializer = LoginRequestOtpSerializer(data=request.data)
        if serializer.is_valid():
            result = send_login_otp(serializer.validated_data, auth)
            return Response(result["data"], status=result["status_code"])
        return Response(serializer.errors, status=400)


class LoginVerifyOtpView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="Login Step 2: Verify OTP (Final)",
        security=[{'Bearer': []}],
        request_body=LoginVerifyOtpSerializer
    )
    def post(self, request):
        auth = request.headers.get("Authorization")
        serializer = LoginVerifyOtpSerializer(data=request.data)
        
        if serializer.is_valid():
            result = verify_login_otp(serializer.validated_data, auth)
            
            # 🪄 THE MAGIC TRICK: Save the X-Token to the backend cache for 30 minutes
            if result["status_code"] == 200 and "token" in result["data"]:
                cache.set("my_saved_x_token", result["data"]["token"], timeout=1800)
                print("✅ X-Token successfully saved to Django cache!")
                
            return Response(result["data"], status=result["status_code"])
            
        return Response(serializer.errors, status=400)
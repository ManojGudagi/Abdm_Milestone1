from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.core.cache import cache

from milestone1.profile_update.serializers.profile_serializers import (
    ProfileRequestOtpSerializer,
    ProfileVerifySerializer,
    ProfileEmailLinkSerializer
)
from milestone1.profile_update.services.profile_services import (
    profile_request_otp_service,
    profile_verify_service,
    profile_email_link_service
)

class ProfileRequestOtpView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(operation_summary="Profile Update Step 1: Request OTP", security=[{'Bearer': []}], request_body=ProfileRequestOtpSerializer)
    def post(self, request):
        auth = request.headers.get("Authorization")
        
        # 🤖 Automatically grab the token from the cache
        x_token = cache.get("my_saved_x_token")
        if not x_token:
            return Response(
                {"error": "No X-token found! You must run the Login API first."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        # Format it cleanly for the government gateway
        formatted_x_token = f"Bearer {x_token}"
        
        serializer = ProfileRequestOtpSerializer(data=request.data)
        if serializer.is_valid():
            result = profile_request_otp_service(serializer.validated_data, auth, formatted_x_token)
            return Response(result["data"], status=result["status_code"])
        return Response(serializer.errors, status=400)


class ProfileVerifyView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(operation_summary="Profile Update Step 2: Verify Action", security=[{'Bearer': []}], request_body=ProfileVerifySerializer)
    def post(self, request):
        auth = request.headers.get("Authorization")
        
        # 🤖 Automatically grab the token from the cache
        x_token = cache.get("my_saved_x_token")
        if not x_token:
            return Response(
                {"error": "No X-token found! You must run the Login API first."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        formatted_x_token = f"Bearer {x_token}"
        
        serializer = ProfileVerifySerializer(data=request.data)
        if serializer.is_valid():
            result = profile_verify_service(serializer.validated_data, auth, formatted_x_token)
            return Response(result["data"], status=result["status_code"])
        return Response(serializer.errors, status=400)


class ProfileEmailLinkView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(operation_summary="Profile Update: Request Email Link", security=[{'Bearer': []}], request_body=ProfileEmailLinkSerializer)
    def post(self, request):
        auth = request.headers.get("Authorization")
        
        # 🤖 Automatically grab the token from the cache
        x_token = cache.get("my_saved_x_token")
        if not x_token:
            return Response(
                {"error": "No X-token found! You must run the Login API first."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        formatted_x_token = f"Bearer {x_token}"
        
        serializer = ProfileEmailLinkSerializer(data=request.data)
        if serializer.is_valid():
            result = profile_email_link_service(serializer.validated_data, auth, formatted_x_token)
            return Response(result["data"], status=result["status_code"])
        return Response(serializer.errors, status=400)
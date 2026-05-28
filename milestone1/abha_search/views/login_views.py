from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

# Import your serializers and services here...
from milestone1.abha_search.serializers.login_serializers import (
    SearchAbhaSerializer,
    SearchRequestOtpSerializer,
    SearchVerifyOtpSerializer
)
from milestone1.abha_search.services.login_services import (
    search_abha_service,
    search_request_otp_service,
    search_verify_otp_service
)

class SearchAbhaView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(operation_summary="Find ABHA Step 1: Search", security=[{'Bearer': []}], request_body=SearchAbhaSerializer)
    def post(self, request):
        auth = request.headers.get("Authorization")
        serializer = SearchAbhaSerializer(data=request.data)
        if serializer.is_valid():
            result = search_abha_service(serializer.validated_data, auth)
            return Response(result["data"], status=result["status_code"])
        return Response(serializer.errors, status=400)


class SearchRequestOtpView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(operation_summary="Find ABHA Step 2: Request OTP", security=[{'Bearer': []}], request_body=SearchRequestOtpSerializer)
    def post(self, request):
        auth = request.headers.get("Authorization")
        serializer = SearchRequestOtpSerializer(data=request.data)
        if serializer.is_valid():
            result = search_request_otp_service(serializer.validated_data, auth)
            return Response(result["data"], status=result["status_code"])
        return Response(serializer.errors, status=400)


class SearchVerifyOtpView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(operation_summary="Find ABHA Step 3: Verify OTP (Final)", security=[{'Bearer': []}], request_body=SearchVerifyOtpSerializer)
    def post(self, request):
        auth = request.headers.get("Authorization")
        serializer = SearchVerifyOtpSerializer(data=request.data)
        if serializer.is_valid():
            result = search_verify_otp_service(serializer.validated_data, auth)
            return Response(result["data"], status=result["status_code"])
        return Response(serializer.errors, status=400)
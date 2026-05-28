from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from milestone1.enrollment_dl.serializers.dl_serializers import (
    DlSendOtpSerializer, 
    DlVerifyOtpSerializer, 
    DlDocumentVerifySerializer
)

from milestone1.enrollment_dl.services.dl_services import (
    send_dl_otp, 
    verify_dl_otp, 
    verify_dl_document
)

class DlSendOtpView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="DL Step 1: Send Mobile OTP",
        security=[{'Bearer': []}],
        request_body=DlSendOtpSerializer
    )
    def post(self, request):
        auth = request.headers.get("Authorization")
        serializer = DlSendOtpSerializer(data=request.data)
        if serializer.is_valid():
            result = send_dl_otp(serializer.validated_data, auth)
            return Response(result["data"], status=result["status_code"])
        return Response(serializer.errors, status=400)

class DlVerifyOtpView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="DL Step 2: Verify Mobile OTP",
        security=[{'Bearer': []}],
        request_body=DlVerifyOtpSerializer
    )
    def post(self, request):
        auth = request.headers.get("Authorization")
        serializer = DlVerifyOtpSerializer(data=request.data)
        if serializer.is_valid():
            result = verify_dl_otp(serializer.validated_data, auth)
            return Response(result["data"], status=result["status_code"])
        return Response(serializer.errors, status=400)

class DlDocumentVerifyView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="DL Step 3: Verify Document & Generate ABHA",
        security=[{'Bearer': []}],
        request_body=DlDocumentVerifySerializer
    )
    def post(self, request):
        auth = request.headers.get("Authorization")
        serializer = DlDocumentVerifySerializer(data=request.data)
        if serializer.is_valid():
            result = verify_dl_document(serializer.validated_data, auth)
            return Response(result["data"], status=result["status_code"])
        return Response(serializer.errors, status=400)
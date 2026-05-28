from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from milestone1.enrollment_biometric.serializers.biometric_serializers import FaceAuthStatusSerializer, BiometricEnrolSerializer
from milestone1.enrollment_biometric.services.biometric_services import init_face_auth, check_face_auth_status, enrol_via_biometric

class FaceAuthInitView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="Face Auth: Init Transaction",
        security=[{'Bearer': []}],
        responses={200: "Transaction ID Generated"}
    )
    def post(self, request):
        auth = request.headers.get("Authorization")
        result = init_face_auth(auth)
        return Response(result["data"], status=result["status_code"])

class FaceAuthStatusView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="Face Auth: Check PID Status",
        security=[{'Bearer': []}],
        request_body=FaceAuthStatusSerializer
    )
    def post(self, request):
        auth = request.headers.get("Authorization")
        serializer = FaceAuthStatusSerializer(data=request.data)
        if serializer.is_valid():
            result = check_face_auth_status(serializer.validated_data.get("txnId"), auth)
            return Response(result["data"], status=result["status_code"])
        return Response(serializer.errors, status=400)

class BiometricEnrolView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="Submit Biometric Verification (Fingerprint/Iris/Face)",
        security=[{'Bearer': []}],
        request_body=BiometricEnrolSerializer
    )
    def post(self, request):
        auth = request.headers.get("Authorization")
        serializer = BiometricEnrolSerializer(data=request.data)
        if serializer.is_valid():
            result = enrol_via_biometric(serializer.validated_data, auth)
            return Response(result["data"], status=result["status_code"])
        return Response(serializer.errors, status=400)
import hashlib
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from milestone1.email_verification.serializers.email_serializer import SendEmailVerificationSerializer
from milestone1.email_verification.services.email_service import send_email_verification


class SendEmailVerificationView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="Send Email Verification Link",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email'],
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="The user's email address"),
            },
            example={
                "email": "user@example.com"
            }
        ),
        responses={200: "Email Link Sent", 401: "Unauthorized"}
    )
    def post(self, request):
        try:
            # 1. Grab Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return Response({"error": "Authorization header missing"}, status=status.HTTP_401_UNAUTHORIZED)

            # 2. Retrieve X-Token safely from cache
            raw_token = auth_header.replace("Bearer ", "").strip()
            token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
            x_token = cache.get(f"x_token_{token_hash}")

            if not x_token:
                return Response(
                    {"error": "X-token not found. Please complete mobile/Aadhaar OTP verification first."},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # 3. Validate Email input
            serializer = SendEmailVerificationSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            email = serializer.validated_data.get("email")

            # 4. Fire the Service
            result = send_email_verification(email, auth_header, x_token)

            return Response(result["data"], status=result["status_code"])

        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response(
                {"status": False, "message": "Internal server error", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
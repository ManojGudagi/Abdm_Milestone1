# views/auth_view.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import uuid
from datetime import datetime, timezone
from milestone1.enrollment_aadhaar.serializers.auth_serializer import SessionSerializer
from milestone1.enrollment_aadhaar.services.auth_service import create_session
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
def get_abdm_timestamp():
    # ABDM expects: 2023-05-24T10:50:00.000Z
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

class SessionTokenView(APIView):
    @swagger_auto_schema(
        operation_summary="Generate ABDM Session Token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "clientId": openapi.Schema(type=openapi.TYPE_STRING, default="{{clientId}}"),
                "clientSecret": openapi.Schema(type=openapi.TYPE_STRING, default="{{clientSecret}}"),
                "grantType": openapi.Schema(type=openapi.TYPE_STRING, default="client_credentials"),
            },
        ),
        responses={200: "Token Response"}
    )

    def post(self, request):

        url = "https://dev.abdm.gov.in/api/hiecm/gateway/v3/sessions"

        headers = {
            "Content-Type": "application/json",
            "REQUEST-ID": str(uuid.uuid4()),
            "TIMESTAMP": datetime.utcnow().isoformat(),
            "X-CM-ID": "sbx"
        }

        payload = {
            "clientId": request.data.get("clientId"),
            "clientSecret": request.data.get("clientSecret"),
            "grantType": request.data.get("grantType")
        }

        res = requests.post(url, json=payload, headers=headers)

        return Response(res.json(), status=res.status_code)


class CertificateView(APIView):

    

    def get(self, request):
        print("CERTIFICATE VIEW HIT")

        url = "https://abhasbx.abdm.gov.in/abha/api/v3/profile/public/certificate"

        # 🔐 Get token from Swagger (Authorize button)
        auth_header = request.headers.get("Authorization")

        # ❌ Validate token
        if not auth_header:
            return Response(
                {"error": "Authorization header missing"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # ✅ ABDM required headers
        headers = {
            "REQUEST-ID": str(uuid.uuid4()),
            "TIMESTAMP": get_abdm_timestamp(),
            "Authorization": auth_header,
                 }

        print("TIMESTAMP:", headers["TIMESTAMP"])
        print("AUTH:", auth_header)

        try:
            res = requests.get(url, headers=headers)

            return Response(
                res.json(),
                status=res.status_code
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# class SessionTokenView(APIView):

#     def post(self, request):

#         # ✅ HEADER VALIDATION
#         request_id = request.headers.get("REQUEST-ID")
#         timestamp = request.headers.get("TIMESTAMP")
#         x_cm_id = request.headers.get("X-CM-ID")

#         if not request_id:
#             return Response({"error": "REQUEST-ID missing"}, status=400)

#         if not timestamp:
#             return Response({"error": "TIMESTAMP missing"}, status=400)

#         if not x_cm_id:
#             return Response({"error": "X-CM-ID missing"}, status=400)

#         # Optional validation
#         if x_cm_id not in ["sbx", "abdm"]:
#             return Response({"error": "Invalid X-CM-ID"}, status=400)

#         # ✅ BODY VALIDATION
#         serializer = SessionSerializer(data=request.data)

#         if not serializer.is_valid():
#             return Response(serializer.errors, status=400)

#         response, status_code = create_session(serializer.validated_data)

#         return Response(response, status=status_code)
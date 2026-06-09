from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from milestone1.enrollment_aadhaar.serializers.enrol_serializer import ABHAEnrolSerializer
from milestone1.enrollment_aadhaar.services.jwt_service import verify_token
from milestone1.enrollment_aadhaar.services.enrol_service import enrol_abha
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import uuid
import requests
from datetime import datetime, timezone

def get_abdm_timestamp():
    # ABDM expects: 2023-05-24T10:50:00.000Z
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

class AadhaarEnrolView(APIView):

    @swagger_auto_schema(
        operation_summary="Enroll ABHA",
        request_body=ABHAEnrolSerializer,
        responses={200: "ABHA Created"}
    )
    def post(self, request):
        try:
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return Response(
                    {"error": "Authorization header missing"},
                    status=401
                )

            # We can still run the serializer to validate base schema if you want, 
            # but we will IGNORE serializer.validated_data because it strips nested JSON.
            # Instead, we pull safely from the raw request.data
            raw_data = request.data
            
            try:
                txn_id = raw_data.get('authData', {}).get('otp', {}).get('txnId')
                otp_value = raw_data.get('authData', {}).get('otp', {}).get('otpValue')
                mobile = raw_data.get('authData', {}).get('otp', {}).get('mobile')
                
                if not all([txn_id, otp_value, mobile]):
                    return Response({"error": "Malformed payload. Missing txnId, otpValue, or mobile."}, status=400)
            except AttributeError:
                return Response({"error": "Invalid JSON structure sent from frontend."}, status=400)

            # Construct the EXACT payload ABDM expects
            abdm_payload = {
                "consent": {
                    "code": "abha-enrollment",
                    "version": "1.4"
                },
                "authData": {
                    "authMethods": ["otp"],
                    "otp": {
                        "txnId": str(txn_id),
                        "otpValue": str(otp_value),
                        "mobile": str(mobile)
                    }
                }
            }

            # Generate headers internally
            headers = {
                "Content-Type": "application/json",
                "REQUEST-ID": str(uuid.uuid4()),
                "TIMESTAMP": get_abdm_timestamp(),
                "Authorization": auth_header
            }

            url = "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/byAadhaar"

            # Print to terminal to absolutely guarantee the data is intact
            print("OUTGOING TO ABDM:", abdm_payload)

            api_response = requests.post(
                url=url,
                json=abdm_payload,
                headers=headers
            )

            return Response(
                api_response.json(),
                status=api_response.status_code
            )

        except Exception as e:
            return Response(
                {
                    "status": False,
                    "message": "Internal server error",
                    "error": str(e)
                },
                status=500
            )

class ABHAProfileView(APIView):

    @swagger_auto_schema(
        operation_summary="Get ABHA Profile Details",
        manual_parameters=[
           openapi.Parameter(
                'X-token',
                openapi.IN_HEADER,
                description="X token without Bearer prefix",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
        responses={200: "Profile Details"}
    )
    def get(self, request):
        try:
            # Authorization from header
            auth_header = request.headers.get("Authorization")

            # X-token from header
            x_token = request.headers.get("X-token")

            if not auth_header:
                return Response(
                    {"error": "Authorization header missing"},
                    status=401
                )

            if not x_token:
                return Response(
                    {"error": "X-token header missing"},
                    status=401
                )

            url = "https://abhasbx.abdm.gov.in/abha/api/v3/profile/account"

            headers = {
                "Content-Type": "application/json",
                "Authorization": auth_header,
                "X-token": f"Bearer {x_token}",
                "REQUEST-ID": str(uuid.uuid4()),
                "TIMESTAMP": get_abdm_timestamp()
            }

            api_response = requests.get(
                url=url,
                headers=headers
            )

            return Response(
                api_response.json(),
                status=api_response.status_code
            )

        except Exception as e:
            return Response(
                {
                    "status": False,
                    "message": "Internal server error",
                    "error": str(e)
                },
                status=500
            )

class DownloadProfileView(APIView):

    @swagger_auto_schema(
        operation_summary="Download Profile",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer Access Token",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'X-token',
                openapi.IN_HEADER,
                description="X token without Bearer prefix",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
        responses={200: "ABHA Card Downloaded"}
    )
    def get(self, request):
        try:
            # Authorization from header
            auth_header = request.headers.get("Authorization")

            # X-token from header
            x_token = request.headers.get("X-token")

            if not auth_header:
                return Response(
                    {"error": "Authorization header missing"},
                    status=401
                )

            if not x_token:
                return Response(
                    {"error": "X-token header missing"},
                    status=401
                )

            url = "https://abhasbx.abdm.gov.in/abha/api/v3/profile/account/abha-card"

            headers = {
                "Content-Type": "application/json",
                "Authorization": auth_header,
                "X-token": f"Bearer {x_token}",
                "REQUEST-ID": str(uuid.uuid4()),
                "TIMESTAMP": get_abdm_timestamp()
            }

            api_response = requests.get(
                url=url,
                headers=headers
            )

            return HttpResponse(
                    api_response.content,
                    content_type=api_response.headers.get(
                        'Content-Type',
                        'application/pdf'
                    )
                )

        except Exception as e:
            return Response(
                {
                    "status": False,
                    "message": "Internal server error",
                    "error": str(e)
                },
                status=500
            )
# milestone1/enrollment_aadhaar/views/abha_address_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from milestone1.abha_profile.services.abha_address_service import get_abha_suggestions, create_abha_address
from milestone1.abha_profile.serializers.abha_address_serializer import CreateAbhaAddressSerializer

# =========================================================
# ✅ 6A: ABHA SUGGESTION VIEW 
# =========================================================
class AbhaSuggestionView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="Get ABHA Address Suggestions",
        security=[{'Bearer': []}],  # 👈 Tells Swagger to use the global Authorize button!
        manual_parameters=[
            openapi.Parameter('txnId', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True, description="Active Transaction ID")
        ],
        responses={200: "Suggestions Retrieved"}
    )
    def get(self, request):
        # We still extract it from the headers in the background
        auth_header = request.headers.get("Authorization")
        txn_id = request.query_params.get("txnId")

        if not auth_header or not txn_id:
            return Response({"error": "Authorization header and txnId query parameter are required"}, status=status.HTTP_400_BAD_REQUEST)

        result = get_abha_suggestions(txn_id, auth_header)
        return Response(result["data"], status=result["status_code"])

# =========================================================
# ✅ 6B: CREATE ABHA ADDRESS VIEW 
# =========================================================
class CreateAbhaAddressView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="Create Custom ABHA Address",
        security=[{'Bearer': []}],  # 👈 Tells Swagger to use the global Authorize button!
        request_body=CreateAbhaAddressSerializer,
        responses={200: "ABHA Created Successfully"}
    )
    def post(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return Response({"error": "Authorization header missing"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CreateAbhaAddressSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        txn_id = serializer.validated_data.get("txnId")
        abha_address = serializer.validated_data.get("abhaAddress")

        result = create_abha_address(txn_id, abha_address, auth_header)
        return Response(result["data"], status=result["status_code"])
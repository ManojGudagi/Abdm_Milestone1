from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.core.cache import cache

# ✅ Clean absolute imports starting from the milestone2 folder
from milestone2.gateway_auth.serializers.auth_serializer import GenerateAuthTokenSerializer
from milestone2.gateway_auth.services.auth_service import generate_gateway_token_service

class GenerateAuthTokenView(APIView):
    @swagger_auto_schema(
        operation_summary="Milestone 2: Generate Gateway Auth Token",
        request_body=GenerateAuthTokenSerializer,
        responses={202: "Token Generated"}
    )
    def post(self, request):
        serializer = GenerateAuthTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        client_id = serializer.validated_data["clientId"]
        client_secret = serializer.validated_data["clientSecret"]

        response_data, status_code = generate_gateway_token_service(client_id, client_secret)

        if status_code in (200, 202) and "accessToken" in response_data:
            access_token = response_data["accessToken"]
            cache.set("abdm_gateway_token", access_token, timeout=1140)
            print("✅ Gateway Token successfully saved to Django cache!")

        return Response(response_data, status=status_code)
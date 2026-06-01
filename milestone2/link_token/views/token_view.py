from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from milestone2.link_token.serializers.token_serializer import GenerateLinkTokenSerializer
from milestone2.link_token.services.token_service import generate_link_token_service
from milestone2.utils import HasGatewayToken # ✅ The Security Bouncer

class GenerateLinkTokenView(APIView):
    # ✅ Lock the endpoint
    permission_classes = [HasGatewayToken]

    @swagger_auto_schema(
        operation_summary="Milestone 2 (4.3.1): Generate Link Token",
        request_body=GenerateLinkTokenSerializer,
        responses={202: "Accepted"}
    )
    def post(self, request):
        serializer = GenerateLinkTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        # Extract the HIP ID so we can pass it to the headers in the service
        validated_data = serializer.validated_data
        hip_id = validated_data.pop("hipId")

        # The remaining validated_data exactly matches the required ABDM JSON body
        response_data, status_code = generate_link_token_service(validated_data, hip_id)

        return Response(response_data, status=status_code)
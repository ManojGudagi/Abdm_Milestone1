from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from milestone2.care_context.serializers.context_serializer import LinkCareContextSerializer
from milestone2.care_context.services.context_service import link_care_context_service
from milestone2.utils import HasGatewayToken

class LinkCareContextView(APIView):
    # ✅ Lock the endpoint
    permission_classes = [HasGatewayToken]

    @swagger_auto_schema(
        operation_summary="Milestone 2 (4.3.3): Link Care Context",
        request_body=LinkCareContextSerializer,
        responses={202: "Accepted"}
    )
    def post(self, request):
        serializer = LinkCareContextSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        validated_data = serializer.validated_data
        
        # Pop the header variables out so they don't get sent in the JSON body!
        hip_id = validated_data.pop("hipId")
        link_token = validated_data.pop("linkToken")

        # The remaining validated_data is exactly what ABDM expects in the body
        response_data, status_code = link_care_context_service(validated_data, hip_id, link_token)

        return Response(response_data, status=status_code)
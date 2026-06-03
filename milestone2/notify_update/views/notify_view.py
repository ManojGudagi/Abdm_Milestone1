from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from milestone2.notify_update.serializers.notify_serializer import NotifyCareContextUpdateSerializer
from milestone2.notify_update.services.notify_service import notify_update_service
from milestone2.utils import HasGatewayToken

class NotifyCareContextUpdateView(APIView):
    """API 4.3.6: Send the notification."""
    # ✅ Lock the endpoint
    permission_classes = [HasGatewayToken]

    @swagger_auto_schema(
        operation_summary="Milestone 2 (4.3.6): Notify Care Context Update",
        request_body=NotifyCareContextUpdateSerializer,
        responses={202: "Accepted"}
    )
    def post(self, request):
        serializer = NotifyCareContextUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        validated_data = serializer.validated_data
        
        # Extract the HIP ID so it doesn't accidentally get sent inside the JSON body
        hip_id = validated_data.pop("hipId")

        # The remaining validated_data exactly matches the nested JSON structure ABDM requires
        response_data, status_code = notify_update_service(validated_data, hip_id)
        
        return Response(response_data, status=status_code)
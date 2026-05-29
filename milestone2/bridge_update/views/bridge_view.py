from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from milestone2.utils import HasGatewayToken

from milestone2.bridge_update.serializers.bridge_serializer import UpdateBridgeUrlSerializer
from milestone2.bridge_update.services.bridge_service import update_bridge_url_service

class UpdateBridgeUrlView(APIView):
    # ✅ Lock the door!
    permission_classes = [HasGatewayToken] 

    @swagger_auto_schema(
        operation_summary="Milestone 2: Update Bridge URL",
        request_body=UpdateBridgeUrlSerializer,
        responses={202: "Accepted"}
    )
    
    def patch(self, request):
        serializer = UpdateBridgeUrlSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        target_url = serializer.validated_data["url"]
        
        # Call the service (No token needed, the service fetches it!)
        response_data, status_code = update_bridge_url_service(target_url)

        return Response(response_data, status=status_code)
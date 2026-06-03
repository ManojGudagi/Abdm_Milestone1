from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from milestone2.hiu_discover.serializers.discover_serializer import OnDiscoverCallbackSerializer
from milestone2.hiu_discover.services.discover_service import process_on_discover_callback

class OnDiscoverCallbackView(APIView):
    # ⚠️ DO NOT add HasGatewayToken here! 
    # ABDM is sending this to us, so they won't have our internal token.
    permission_classes = [] 

    @swagger_auto_schema(
        operation_summary="Milestone 3 (5.3.4): Webhook - On Discover",
        request_body=OnDiscoverCallbackSerializer,
        responses={200: "OK"}
    )
    def post(self, request):
        serializer = OnDiscoverCallbackSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        # Process the incoming webhook and log it
        response_data, status_code = process_on_discover_callback(serializer.validated_data)

        # Return 200 OK so ABDM knows we safely received the records
        return Response(response_data, status=status_code)
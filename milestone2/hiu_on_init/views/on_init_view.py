from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from milestone2.hiu_on_init.serializers.on_init_serializer import HiuOnInitCallbackSerializer
from milestone2.hiu_on_init.services.on_init_service import process_hiu_on_init_callback

class HiuOnInitCallbackView(APIView):
    # ⚠️ Unlocked for inbound webhook
    permission_classes = [] 

    @swagger_auto_schema(
        operation_summary="Milestone 3 (5.3.8): Webhook - On Init Response",
        request_body=HiuOnInitCallbackSerializer,
        responses={202: "Accepted"}
    )
    def post(self, request):
        serializer = HiuOnInitCallbackSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        # Process the incoming webhook and log it to terminal
        response_data, status_code = process_hiu_on_init_callback(serializer.validated_data)

        # Return 202 Accepted to ABDM
        return Response(response_data, status=status_code)
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from milestone2.hiu_on_confirm.serializers.on_confirm_serializer import HiuOnConfirmCallbackSerializer
from milestone2.hiu_on_confirm.services.on_confirm_service import process_hiu_on_confirm_callback

class HiuOnConfirmCallbackView(APIView):
    # ⚠️ Unlocked for inbound webhook
    permission_classes = [] 

    @swagger_auto_schema(
        operation_summary="Milestone 3 (5.3.12): Webhook - On Confirm Response",
        request_body=HiuOnConfirmCallbackSerializer,
        responses={202: "Accepted"}
    )
    def post(self, request):
        serializer = HiuOnConfirmCallbackSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        # Process the incoming webhook and log it to terminal
        response_data, status_code = process_hiu_on_confirm_callback(serializer.validated_data)

        # Return 202 Accepted to ABDM
        return Response(response_data, status=status_code)
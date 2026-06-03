from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from milestone2.sms_notify.serializers.sms_serializer import SmsNotifySerializer
from milestone2.sms_notify.services.sms_service import send_sms_notification_service
from milestone2.utils import HasGatewayToken

class SendSmsNotificationView(APIView):
    # ✅ Lock the endpoint
    permission_classes = [HasGatewayToken]

    @swagger_auto_schema(
        operation_summary="Milestone 2 (4.3.8): SMS Notification to Patient",
        request_body=SmsNotifySerializer,
        responses={202: "Accepted"}
    )
    def post(self, request):
        serializer = SmsNotifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        # Extract just the 'notification' dictionary from the serializer
        notification_data = serializer.validated_data.get("notification")

        response_data, status_code = send_sms_notification_service(notification_data)
        
        return Response(response_data, status=status_code)
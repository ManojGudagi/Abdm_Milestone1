from rest_framework import serializers

class SmsHipDetailSerializer(serializers.Serializer):
    id = serializers.CharField(required=True, help_text="e.g., TestClinicHIP or IN2810014366")
    name = serializers.CharField(required=True, help_text="e.g., ABC Hospital")

class SmsNotificationDetailSerializer(serializers.Serializer):
    phoneNo = serializers.CharField(required=True, help_text="10-digit mobile number")
    hip = SmsHipDetailSerializer()

class SmsNotifySerializer(serializers.Serializer):
    # We only ask the user for the notification data. 
    # The view/service will automatically generate the requestId and timestamp for the body!
    notification = SmsNotificationDetailSerializer()
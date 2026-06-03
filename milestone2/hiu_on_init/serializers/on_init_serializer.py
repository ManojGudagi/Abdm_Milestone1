from rest_framework import serializers

class HiuInitMetaSerializer(serializers.Serializer):
    communicationMedium = serializers.CharField(required=True, help_text="e.g., MOBILE")
    communicationHint = serializers.CharField(required=True, help_text="e.g., OTP")
    communicationExpiry = serializers.CharField(required=True, help_text="e.g., 2023-12-30T12:01:55.324Z")

class HiuInitLinkSerializer(serializers.Serializer):
    referenceNumber = serializers.CharField(required=True)
    authenticationType = serializers.CharField(required=True, help_text="e.g., MEDIATE")
    meta = HiuInitMetaSerializer()

class HiuInitErrorSerializer(serializers.Serializer):
    code = serializers.IntegerField(required=True)
    message = serializers.CharField(required=True)

class HiuInitResponseSerializer(serializers.Serializer):
    requestId = serializers.CharField(required=True)

class HiuOnInitCallbackSerializer(serializers.Serializer):
    transactionId = serializers.CharField(required=True)
    # Both link and error are optional depending on if the request was successful
    link = HiuInitLinkSerializer(required=False)
    error = HiuInitErrorSerializer(required=False)
    response = HiuInitResponseSerializer(required=True)
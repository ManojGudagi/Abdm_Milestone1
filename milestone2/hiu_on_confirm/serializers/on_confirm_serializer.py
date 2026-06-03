from rest_framework import serializers

class ConfirmCareContextSerializer(serializers.Serializer):
    referenceNumber = serializers.CharField(required=True, help_text="e.g., 1234")
    display = serializers.CharField(required=False, allow_blank=True, help_text="e.g., 1234-display")

class ConfirmPatientSerializer(serializers.Serializer):
    # This is the Link reference number
    referenceNumber = serializers.CharField(required=True, help_text="e.g., 4336268d-89a3-4c84-8674-aef42092d9fc")
    display = serializers.CharField(required=False, allow_blank=True, help_text="e.g., abcdefgdisplay")
    careContexts = ConfirmCareContextSerializer(many=True)
    hiType = serializers.CharField(required=True, help_text="e.g., PRESCRIPTION")
    count = serializers.IntegerField(required=True)

class ConfirmResponseSerializer(serializers.Serializer):
    requestId = serializers.CharField(required=True, help_text="e.g., f207e461-1994-4274-9b86-554384f170ab")

class HiuOnConfirmCallbackSerializer(serializers.Serializer):
    # The payload expects 'patient' as a list
    patient = ConfirmPatientSerializer(many=True)
    response = ConfirmResponseSerializer(required=True)
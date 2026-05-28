from rest_framework import serializers

class CreateAbhaAddressSerializer(serializers.Serializer):
    txnId = serializers.CharField(
        required=True, 
        help_text="Active Transaction ID from the mobile verify step"
    )
    abhaAddress = serializers.CharField(
        required=True, 
        help_text="Desired ABHA Address (e.g., firstname_123)"
    )
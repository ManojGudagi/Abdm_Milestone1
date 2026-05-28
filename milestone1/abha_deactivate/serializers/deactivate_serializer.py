from rest_framework import serializers

class GenerateDeactivateOtpSerializer(serializers.Serializer):
    ABHANumber = serializers.CharField(
        required=True, 
        help_text="Plaintext ABHA number (e.g., 91-XXXX-XXXX-XXXX)"
    )

class VerifyDeactivateOtpSerializer(serializers.Serializer):
    txnId = serializers.CharField(required=True)
    otpValue = serializers.CharField(
        required=True, 
        help_text="Plaintext OTP received by the user"
    )
    # ✅ New field required for deactivation
    reasons = serializers.ListField(
        child=serializers.CharField(),
        required=True,
        help_text='List of reasons. Example: ["Lost phone", "No longer needed"]'
    )
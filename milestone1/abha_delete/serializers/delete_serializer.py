from rest_framework import serializers

class GenerateDeleteOtpSerializer(serializers.Serializer):
    # The user provides their ABHA number, which we will encrypt before sending to ABDM
    ABHANumber = serializers.CharField(
        required=True, 
        help_text="Plaintext ABHA number (e.g., 91-XXXX-XXXX-XXXX)"
    )

class VerifyDeleteOtpSerializer(serializers.Serializer):
    txnId = serializers.CharField(required=True)
    otpValue = serializers.CharField(
        required=True, 
        help_text="Plaintext OTP received by the user"
    )
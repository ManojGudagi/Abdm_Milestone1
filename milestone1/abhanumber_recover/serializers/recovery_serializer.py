from rest_framework import serializers

class GenerateRecoveryOtpSerializer(serializers.Serializer):
    # ✅ This is the "clue" the frontend must send
    loginHint = serializers.ChoiceField(
        choices=["aadhaar", "mobile"], 
        help_text="Must be exactly 'aadhaar' or 'mobile'"
    )
    loginId = serializers.CharField(
        required=True, 
        help_text="Plaintext Aadhaar or Mobile number"
    )

class VerifyRecoveryOtpSerializer(serializers.Serializer):
    # ✅ We also need the clue here to send the right scope to ABDM
    loginHint = serializers.ChoiceField(
        choices=["aadhaar", "mobile"], 
        help_text="Must be exactly 'aadhaar' or 'mobile'"
    )
    txnId = serializers.CharField(required=True)
    otpValue = serializers.CharField(required=True, help_text="Plaintext OTP entered by the user")
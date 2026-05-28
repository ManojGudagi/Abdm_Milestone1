from rest_framework import serializers

class LoginRequestOtpSerializer(serializers.Serializer):
    loginHint = serializers.ChoiceField(
        choices=['abha-number','aadhaar'],
        help_text="Choose how the user is logging in (Mobile flow disabled)."
    )
    loginId = serializers.CharField(
        required=True,
        help_text="Plain text ID (Aadhaar number or ABHA number)"
    )
    otpSystem = serializers.ChoiceField(
        choices=['aadhaar', 'abdm'],
        help_text="Use 'aadhaar' for Aadhaar OTP, 'abdm' for ABHA OTP"
    )

class LoginVerifyOtpSerializer(serializers.Serializer):
    loginHint = serializers.ChoiceField(
        choices=['aadhaar', 'abha-number'],
        help_text="Must match the hint you used in Step 1."
    )
    txnId = serializers.CharField(required=True)
    otpValue = serializers.CharField(required=True, help_text="Plain 6-digit OTP")
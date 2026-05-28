from rest_framework import serializers

class ProfileRequestOtpSerializer(serializers.Serializer):
    action = serializers.ChoiceField(
        choices=['update-mobile', 'delete', 'deactivate', 're-kyc'],
        help_text="What are you trying to do to this profile?"
    )
    loginHint = serializers.ChoiceField(
        choices=['mobile', 'abha-number'],
        help_text="mobile (for update-mobile) OR abha-number (for delete/deactivate/re-kyc)"
    )
    loginId = serializers.CharField(
        required=True,
        help_text="Plain text Mobile Number or ABHA Number. Backend will encrypt it."
    )
    otpSystem = serializers.ChoiceField(
        choices=['abdm', 'aadhaar'],
        default='abdm'
    )

class ProfileVerifySerializer(serializers.Serializer):
    action = serializers.ChoiceField(
        choices=['update-mobile', 'delete', 'deactivate', 're-kyc'],
        help_text="Must match the action from Step 1"
    )
    txnId = serializers.CharField(required=True)
    authMethod = serializers.ChoiceField(
        choices=['otp', 'password'],
        default='otp'
    )
    authValue = serializers.CharField(
        required=True, 
        help_text="Plain text 6-digit OTP -OR- your plain text Password. Backend will encrypt it."
    )
    # 👇 ADD THIS FIELD
    otpSystem = serializers.ChoiceField(
        choices=['abdm', 'aadhaar'],
        default='abdm',
        help_text="Required to reconstruct the correct scope array for the gateway."
    )

class ProfileEmailLinkSerializer(serializers.Serializer):
    loginId = serializers.CharField(
        required=True, 
        help_text="Plain text Email Address. Backend will encrypt it."
    )
    txnId = serializers.CharField(required=True, help_text="Transaction ID from previous step")
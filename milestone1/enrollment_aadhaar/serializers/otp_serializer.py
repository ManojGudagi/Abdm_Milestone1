from rest_framework import serializers

class AadhaarOtpRequestSerializer(serializers.Serializer):
    txnId = serializers.CharField(required=False, allow_blank=True)
    scope = serializers.ListField(child=serializers.CharField())
    loginHint = serializers.CharField()
    loginId = serializers.CharField()
    otpSystem = serializers.CharField()
    VALID_SCOPES = [
        "abha-enrol",
        "dl-flow",
        "mobile-verify",
        "email-verify"
    ]

    VALID_OTP_SYSTEMS = [
        "aadhaar",
        "abdm"
    ]
     # 🔍 Scope validation
    def validate_scope(self, value):
        if not value:
            raise serializers.ValidationError("Scope cannot be empty")

        for scope in value:
            if scope not in self.VALID_SCOPES:
                raise serializers.ValidationError(f"Invalid scope: {scope}")

        return value

    # 🔍 loginHint validation
    def validate_loginHint(self, value):
        if value.lower() != "aadhaar":
            raise serializers.ValidationError("loginHint must be 'aadhaar'")
        return value

    # 🔍 otpSystem validation
    def validate_otpSystem(self, value):
        if value.lower() not in self.VALID_OTP_SYSTEMS:
            raise serializers.ValidationError("Invalid otpSystem")
        return value

    # 🔍 loginId validation
    def validate_loginId(self, value):
        if not value:
            raise serializers.ValidationError("loginId is required")
        return value

class OTPRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=10)

class AadhaarOTPVerifySerializer(serializers.Serializer):
    txnId = serializers.CharField()
    otp = serializers.CharField()

class SendOtpSerializer(serializers.Serializer):
    loginId = serializers.CharField(required=True)
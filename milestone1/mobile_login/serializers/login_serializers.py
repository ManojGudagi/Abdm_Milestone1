from rest_framework import serializers

class MobileRequestOtpSerializer(serializers.Serializer):
    mobileNumber = serializers.CharField(
        required=True,
        help_text="10-digit Mobile Number"
    )

class MobileVerifyOtpSerializer(serializers.Serializer):
    txnId = serializers.CharField(required=True)
    otpValue = serializers.CharField(required=True, help_text="6-digit OTP received on mobile")

class MobileVerifyUserSerializer(serializers.Serializer):
    ABHANumber = serializers.CharField(
        required=True, 
        help_text="14-digit ABHA Number selected from Step 2 response (e.g., 91-1234-5678-XXXX)"
    )
    txnId = serializers.CharField(required=True, help_text="The NEW txnId from Step 2")
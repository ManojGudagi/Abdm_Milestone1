# milestone1/enrollment_mobile/serializers/mobile_otp_serializer.py

from rest_framework import serializers


# =========================================================
# ✅ SEND MOBILE OTP SERIALIZER
# =========================================================
class MobileOtpRequestSerializer(serializers.Serializer):

    txnId = serializers.CharField(
        default=""
    )

    scope = serializers.ListField(
        child=serializers.CharField(),
        default=["abha-enrol", "mobile-verify"]
    )

    loginHint = serializers.CharField(
        default="mobile"
    )

    loginId = serializers.CharField(
        default=""
    )

    otpSystem = serializers.CharField(
        default="abdm"
    )


# =========================================================
# ✅ VERIFY OTP SERIALIZER
# =========================================================
class OTPSerializer(serializers.Serializer):

    timeStamp = serializers.CharField(
        default="2026-05-12T13:00:00.000Z"
    )

    txnId = serializers.CharField(
        default=""
    )

    otpValue = serializers.CharField(
        default=""
    )


class AuthDataSerializer(serializers.Serializer):

    authMethods = serializers.ListField(
        child=serializers.CharField(),
        default=["otp"]
    )

    otp = OTPSerializer()


from rest_framework import serializers

class MobileOtpVerifySerializer(serializers.Serializer):
    txnId = serializers.CharField(
        required=True, 
        error_messages={"required": "txnId is required to verify OTP."}
    )
    otpValue = serializers.CharField(
        required=True, 
        error_messages={"required": "otpValue is required."}
    )
    mobile = serializers.CharField(
        required=False, 
        allow_blank=True, 
        default=""
    )
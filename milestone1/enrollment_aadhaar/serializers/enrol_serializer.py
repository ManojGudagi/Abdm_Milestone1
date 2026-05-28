from rest_framework import serializers


class OTPDetailsSerializer(serializers.Serializer):
    txnId = serializers.CharField()
    otpValue = serializers.CharField()
    mobile = serializers.CharField()


class ABHAAuthDataSerializer(serializers.Serializer):
    authMethods = serializers.ListField(
        child=serializers.CharField()
    )
    otp = OTPDetailsSerializer()


class ABHAConsentSerializer(serializers.Serializer):
    code = serializers.CharField()
    version = serializers.CharField()


class ABHAEnrolSerializer(serializers.Serializer):
    authData = ABHAAuthDataSerializer()
    consent = ABHAConsentSerializer()
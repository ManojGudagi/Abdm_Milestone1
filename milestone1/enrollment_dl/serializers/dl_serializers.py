from rest_framework import serializers

class DlSendOtpSerializer(serializers.Serializer):
    loginId = serializers.CharField(help_text="Plain 10-digit mobile number")

class DlVerifyOtpSerializer(serializers.Serializer):
    txnId = serializers.CharField()
    otpValue = serializers.CharField(help_text="Plain 6-digit OTP")

class DlDocumentVerifySerializer(serializers.Serializer):
    txnId = serializers.CharField()
    documentId = serializers.CharField(help_text="Driving License Number (e.g., MH1320140019054)")
    firstName = serializers.CharField()
    middleName = serializers.CharField(required=False, allow_blank=True, default="")
    lastName = serializers.CharField()
    dob = serializers.CharField(help_text="YYYY-MM-DD")
    gender = serializers.CharField(help_text="M, F, or O")
    frontSidePhoto = serializers.CharField(help_text="Base64 encoded string of front image")
    backSidePhoto = serializers.CharField(help_text="Base64 encoded string of back image")
    address = serializers.CharField()
    state = serializers.CharField()
    district = serializers.CharField()
    pinCode = serializers.CharField()
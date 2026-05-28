from rest_framework import serializers

class SearchAbhaSerializer(serializers.Serializer):
    searchHint = serializers.ChoiceField(
        choices=['mobile', 'aadhaar'],
        default='mobile',
        help_text="Are you searching by Mobile Number or Aadhaar Number?"
    )
    loginId = serializers.CharField(
        required=True,
        help_text="Plain text 10-digit Mobile or 12-digit Aadhaar"
    )

class SearchRequestOtpSerializer(serializers.Serializer):
    loginHint = serializers.ChoiceField(
        choices=['index'],
        default='index',
        help_text="Strictly required to be 'index' for this flow."
    )
    loginId = serializers.CharField(
        required=True,
        help_text="Type the raw index number here (e.g., '1'). The backend will encrypt it."
    )
    txnId = serializers.CharField(
        required=True,
        help_text="The txnId received from the Step 1 Search response."
    )
    otpSystem = serializers.ChoiceField(
        choices=['abdm', 'aadhaar'],
        default='abdm',
        help_text="Use 'abdm' for Mobile OTP flow, 'aadhaar' for Aadhaar OTP flow."
    )

class SearchVerifyOtpSerializer(serializers.Serializer):
    txnId = serializers.CharField(required=True)
    otpValue = serializers.CharField(required=True, help_text="Plain 6-digit OTP")
    otpSystem = serializers.ChoiceField(
        choices=['abdm', 'aadhaar'],
        default='abdm',
        help_text="Must match what you selected in Step 2 to set the correct scope"
    )
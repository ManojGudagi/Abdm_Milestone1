from rest_framework import serializers

class FaceAuthStatusSerializer(serializers.Serializer):
    txnId = serializers.CharField(required=True, help_text="Transaction ID from the init step")

class BiometricEnrolSerializer(serializers.Serializer):
    # This tells the backend which flow we are doing
    authMethod = serializers.ChoiceField(
        choices=['bio', 'iris', 'face_auth'], 
        help_text="Choose: 'bio' (Fingerprint), 'iris' (Iris Scan), or 'face_auth' (Face Scan)"
    )
    txnId = serializers.CharField(required=True, help_text="Active Transaction ID")
    
    # 🛑 The plain Aadhaar number from the frontend
    aadhaarNumber = serializers.CharField(
        required=True, 
        help_text="Plain text [Aadhaar Redacted] number"
    )
    
    # Optional fields depending on the method
    pid = serializers.CharField(
        required=False, 
        allow_blank=True, 
        help_text="Encrypted PID from device (Required for bio/iris, leave blank for face_auth)"
    )
    mobile = serializers.CharField(
        required=False, 
        allow_blank=True, 
        default="", 
        help_text="Optional alternate mobile number"
    )
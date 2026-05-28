from rest_framework import serializers

class SendEmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True, 
        error_messages={"required": "Email address is required.", "invalid": "Enter a valid email address."}
    )
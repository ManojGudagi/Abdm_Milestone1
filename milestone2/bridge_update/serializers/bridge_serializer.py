from rest_framework import serializers

class UpdateBridgeUrlSerializer(serializers.Serializer):
    url = serializers.URLField(
        required=True,
        help_text="Your Bridge Base URL (e.g., https://webhook.site/your-id)"
    )
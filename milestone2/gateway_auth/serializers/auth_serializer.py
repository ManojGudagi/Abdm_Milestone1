from rest_framework import serializers

class GenerateAuthTokenSerializer(serializers.Serializer):
    clientId = serializers.CharField(required=True)
    clientSecret = serializers.CharField(required=True)
    grantType = serializers.CharField()
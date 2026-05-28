from rest_framework import serializers

class SessionSerializer(serializers.Serializer):
    clientId = serializers.CharField()
    clientSecret = serializers.CharField()
    grantType = serializers.CharField()
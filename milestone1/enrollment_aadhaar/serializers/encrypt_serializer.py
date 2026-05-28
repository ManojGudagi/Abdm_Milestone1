# serializers/encryption_serializer.py

from rest_framework import serializers


class EncryptSerializer(serializers.Serializer):
    data = serializers.CharField()
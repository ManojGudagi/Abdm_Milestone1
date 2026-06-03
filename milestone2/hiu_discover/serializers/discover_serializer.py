from rest_framework import serializers

class DiscoverCareContextSerializer(serializers.Serializer):
    referenceNumber = serializers.CharField(required=True)
    display = serializers.CharField(required=False, allow_blank=True)

class DiscoverPatientSerializer(serializers.Serializer):
    referenceNumber = serializers.CharField(required=True)
    display = serializers.CharField(required=False, allow_blank=True)
    careContexts = DiscoverCareContextSerializer(many=True)
    hiType = serializers.CharField(required=True)
    count = serializers.IntegerField(required=True)

class DiscoverResponseSerializer(serializers.Serializer):
    requestId = serializers.CharField(required=True)

class OnDiscoverCallbackSerializer(serializers.Serializer):
    transactionId = serializers.CharField(required=True)
    patient = DiscoverPatientSerializer(many=True)
    createdAt = serializers.CharField(required=True)
    response = DiscoverResponseSerializer(required=True)
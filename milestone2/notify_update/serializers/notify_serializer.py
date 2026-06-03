from rest_framework import serializers

class PatientIdSerializer(serializers.Serializer):
    id = serializers.CharField(required=True, help_text="e.g., user123@sbx")

class CareContextRefSerializer(serializers.Serializer):
    patientReference = serializers.CharField(required=True, help_text="e.g., batman@tmh")
    careContextReference = serializers.CharField(required=True, help_text="e.g., Episode1")

class HipIdSerializer(serializers.Serializer):
    id = serializers.CharField(required=True, help_text="e.g., demo-hip-261222")

class NotificationDetailSerializer(serializers.Serializer):
    patient = PatientIdSerializer()
    careContext = CareContextRefSerializer()
    hiTypes = serializers.ListField(
        child=serializers.ChoiceField(choices=[
            "PRESCRIPTION", "DiagnosticReport", "OPConsultation", 
            "DischargeSummary", "ImmunizationRecord", 
            "HealthDocumentRecord", "WellnessRecord"
        ]),
        required=True
    )
    date = serializers.CharField(required=True, help_text="ISO Date string, e.g., 2024-05-30T05:21:34.155Z")
    hip = HipIdSerializer()

class NotifyCareContextUpdateSerializer(serializers.Serializer):
    # This is for the X-HIP-ID Header
    hipId = serializers.CharField(required=True, help_text="For X-HIP-ID Header")
    
    # This is the actual JSON Body ABDM expects
    notification = NotificationDetailSerializer()
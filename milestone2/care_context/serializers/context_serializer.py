from rest_framework import serializers

class CareContextDetailSerializer(serializers.Serializer):
    referenceNumber = serializers.CharField(required=True, help_text="e.g., TMH-PUID-001")
    display = serializers.CharField(required=True, help_text="e.g., display 1")

class PatientDetailSerializer(serializers.Serializer):
    referenceNumber = serializers.CharField(required=True, help_text="e.g., TMH-PUID-001")
    display = serializers.CharField(required=True, help_text="e.g., Display")
    careContexts = CareContextDetailSerializer(many=True)
    hiType = serializers.ChoiceField(
        choices=[
            "PRESCRIPTION", "DiagnosticReport", "OPConsultation", 
            "DischargeSummary", "ImmunizationRecord", 
            "HealthDocumentRecord", "WellnessRecord"
        ],
        required=True
    )
    count = serializers.IntegerField(required=True, help_text="Number of records, e.g., 1")

class LinkCareContextSerializer(serializers.Serializer):
    # --- These two fields are for the Headers ---
    hipId = serializers.CharField(required=True, help_text="Facility ID (e.g., IN2810014366)")
    linkToken = serializers.CharField(required=True, help_text="The X-LINK-TOKEN")
    
    # --- These fields are for the JSON Body ---
    abhaAddress = serializers.CharField(required=True, help_text="Patient's ABHA Address")
    abhaNumber = serializers.CharField(required=False, allow_blank=True, help_text="14-digit ABHA Number")
    patient = PatientDetailSerializer(many=True)
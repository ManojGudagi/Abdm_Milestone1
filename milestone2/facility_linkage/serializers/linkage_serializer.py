from rest_framework import serializers
from django.core.validators import RegexValidator

class BridgeDetailSerializer(serializers.Serializer):
    bridgeId = serializers.CharField(
        required=True, 
        help_text="Valid Bridge Id to be linked"
    )
    hipName = serializers.CharField(
        required=True,
        max_length=15,
        validators=[RegexValidator(r'^[a-zA-Z0-9\s]+$', "No special characters allowed.")],
        help_text="Max 15 chars, alphanumeric (e.g., XYZ BRIDGE)"
    )
    type = serializers.ChoiceField(
        choices=["HIP", "HIU"], 
        required=True,
        help_text="HIP or HIU"
    )
    # ✅ Changed from 'Active' to 'active' (lowercase)
    active = serializers.BooleanField(
        required=True,
        help_text="True or false"
    )

class FacilityLinkageSerializer(serializers.Serializer):
    facilityId = serializers.CharField(
        required=True,
        validators=[RegexValidator(r'^IN', "Facility ID must start with 'IN'")],
        help_text="Starts with IN and of 12 characters"
    )
    facilityName = serializers.CharField(
        required=True,
        validators=[RegexValidator(r'^[a-zA-Z0-9\s]+$', "Alphanumeric only")],
        help_text="Name of the facility"
    )
    # ✅ Changed from 'bridges' to 'HRP' (This is the exact key ABDM expects)
    HRP = BridgeDetailSerializer(many=True)
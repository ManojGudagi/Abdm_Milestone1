from rest_framework import serializers

class GenerateLinkTokenSerializer(serializers.Serializer):
    # We take the HIP ID here in the body so you can easily type it into Swagger
    hipId = serializers.CharField(
        required=True, 
        help_text="The Facility ID (e.g., IN2810014366)"
    )
    abhaAddress = serializers.CharField(
        required=False, 
        allow_blank=True,
        help_text="Patient's ABHA Address (e.g., user@sbx)"
    )
    abhaNumber = serializers.CharField(
        required=False, 
        allow_blank=True,
        help_text="Patient's 14-digit ABHA Number"
    )
    name = serializers.CharField(
        required=True, 
        help_text="Full name: First Name | Middle Name | Last Name"
    )
    gender = serializers.ChoiceField(
        choices=["M", "F", "O"], 
        required=True,
        help_text="M, F, or O"
    )
    yearOfBirth = serializers.IntegerField(
        required=True,
        help_text="e.g., 1990"
    )

    def validate(self, data):
        """Ensure at least one ABHA identifier is provided."""
        abha_address = data.get("abhaAddress")
        abha_number = data.get("abhaNumber")

        if not abha_address and not abha_number:
            raise serializers.ValidationError(
                "You must provide either an abhaAddress or an abhaNumber."
            )
        return data
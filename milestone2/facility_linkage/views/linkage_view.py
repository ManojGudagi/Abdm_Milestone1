from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from milestone2.utils import HasGatewayToken

# ✅ Clean absolute imports mapping to your new folder
from milestone2.facility_linkage.serializers.linkage_serializer import FacilityLinkageSerializer
from milestone2.facility_linkage.services.linkage_service import link_facility_service

class LinkFacilityView(APIView):
    permission_classes = [HasGatewayToken]
    @swagger_auto_schema(
        operation_summary="Milestone 2: Facility & Software Linkage",
        request_body=FacilityLinkageSerializer,
        responses={200: "Linked Successfully"}
    )
    def post(self, request):
        serializer = FacilityLinkageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        # Pass the fully validated and structured JSON to the service
        response_data, status_code = link_facility_service(serializer.validated_data)

        return Response(response_data, status=status_code)
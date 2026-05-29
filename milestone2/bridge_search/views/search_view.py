from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from milestone2.utils import HasGatewayToken

# ✅ Absolute import for the service we just wrote
from milestone2.bridge_search.services.search_service import find_bridge_by_service_id

class FindBridgeByServiceIdView(APIView):
    permission_classes = [HasGatewayToken]
    @swagger_auto_schema(
        operation_summary="Milestone 2 (3.2.6): Find Bridge by Service ID",
        responses={200: "Bridge details fetched"}
    )
    # The 'service_id' gets grabbed straight from the URL path!
    def get(self, request, service_id):
        response_data, status_code = find_bridge_by_service_id(service_id)
        return Response(response_data, status=status_code)
    




# Import the second service you just added
from milestone2.bridge_search.services.search_service import find_services_by_bridge_id

class FindServicesByBridgeIdView(APIView):
    permission_classes = [HasGatewayToken]
    @swagger_auto_schema(
        operation_summary="Milestone 2 (3.2.7): Find Services by Bridge ID",
        responses={200: "Services fetched"}
    )
    def get(self, request):
        # No extra variables needed, it just runs!
        response_data, status_code = find_services_by_bridge_id()
        return Response(response_data, status=status_code)
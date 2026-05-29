from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

# ✅ Clean absolute imports
from milestone2.gateway_config.services.config_service import (
    get_openid_configuration_service,
    get_keycloak_certs_service
)

class OpenIdConfigView(APIView):
    @swagger_auto_schema(
        operation_summary="Milestone 2 (3.2.2): OpenID Configuration",
        responses={200: "Configuration fetched"}
    )
    def get(self, request):
        response_data, status_code = get_openid_configuration_service()
        return Response(response_data, status=status_code)


class KeycloakCertsView(APIView):
    @swagger_auto_schema(
        operation_summary="Milestone 2 (3.2.3): Keycloak Certificates",
        responses={200: "Certificates fetched"}
    )
    def get(self, request):
        response_data, status_code = get_keycloak_certs_service()
        return Response(response_data, status=status_code)
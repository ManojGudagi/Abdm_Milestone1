from django.urls import path
from milestone2.gateway_config.views.config_view import (
    OpenIdConfigView,
    KeycloakCertsView
)

urlpatterns = [
    # API 3.2.2
    path('openid-configuration/', OpenIdConfigView.as_view(), name='openid-config'),
    
    # API 3.2.3
    path('certs/', KeycloakCertsView.as_view(), name='keycloak-certs'),
]
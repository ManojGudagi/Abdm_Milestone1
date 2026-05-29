from django.urls import path
from milestone2.gateway_auth.views.auth_view import GenerateAuthTokenView

urlpatterns = [
    path('sessions/', GenerateAuthTokenView.as_view(), name='generate-gateway-token'),
]
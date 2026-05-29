from django.urls import path
from milestone2.bridge_update.views.bridge_view import UpdateBridgeUrlView

urlpatterns = [
    # Using 'patch' to match the HTTP method, but you can name this whatever you like
    path('url/', UpdateBridgeUrlView.as_view(), name='update-bridge-url'),
]
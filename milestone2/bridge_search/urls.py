from django.urls import path
from milestone2.bridge_search.views.search_view import (
    FindBridgeByServiceIdView,
    FindServicesByBridgeIdView
)

urlpatterns = [
    # API 3.2.6 (Requires an ID in the URL)
    path('serviceId/<str:service_id>/', FindBridgeByServiceIdView.as_view(), name='find-bridge-by-service'),
    
    # API 3.2.7 (No ID required)
    path('services/', FindServicesByBridgeIdView.as_view(), name='find-all-services'),
]
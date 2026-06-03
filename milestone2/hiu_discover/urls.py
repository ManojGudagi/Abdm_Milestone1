from django.urls import path
from milestone2.hiu_discover.views.discover_view import OnDiscoverCallbackView

urlpatterns = [
    # Using the exact path requested by the documentation
    path('patient/care-context/on-discover/', OnDiscoverCallbackView.as_view(), name='on-discover-callback'),
]
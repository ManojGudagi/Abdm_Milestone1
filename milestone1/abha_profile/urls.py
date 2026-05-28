from django.urls import path
from milestone1.abha_profile.views.abha_address_view import AbhaSuggestionView, CreateAbhaAddressView

urlpatterns = [
    # ... your existing urls ...
    path('abha/suggestions/', AbhaSuggestionView.as_view(), name='abha-suggestions'),
    path('abha/create-address/', CreateAbhaAddressView.as_view(), name='abha-create-address'),
]
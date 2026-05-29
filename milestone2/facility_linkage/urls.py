from django.urls import path
from milestone2.facility_linkage.views.linkage_view import LinkFacilityView

urlpatterns = [
    path('link-software/', LinkFacilityView.as_view(), name='link-facility'),
]
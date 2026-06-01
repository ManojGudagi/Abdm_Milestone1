from django.urls import path
from milestone2.care_context.views.context_view import LinkCareContextView

urlpatterns = [
    path('link/', LinkCareContextView.as_view(), name='link-care-context'),
]
from django.urls import path
from milestone2.link_token.views.token_view import GenerateLinkTokenView

urlpatterns = [
    path('generate/', GenerateLinkTokenView.as_view(), name='generate-link-token'),
]
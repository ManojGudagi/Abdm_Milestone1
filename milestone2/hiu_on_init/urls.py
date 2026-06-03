from django.urls import path
from milestone2.hiu_on_init.views.on_init_view import HiuOnInitCallbackView

urlpatterns = [
    # API URL matches the documentation exactly
    path('patient/care-context/on-init/', HiuOnInitCallbackView.as_view(), name='hiu-on-init-callback'),
]
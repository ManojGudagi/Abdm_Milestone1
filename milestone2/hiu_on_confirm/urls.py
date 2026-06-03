from django.urls import path
from milestone2.hiu_on_confirm.views.on_confirm_view import HiuOnConfirmCallbackView

urlpatterns = [
    # API URL matches the documentation exactly
    path('patient/care-context/on-confirm/', HiuOnConfirmCallbackView.as_view(), name='hiu-on-confirm-callback'),
]
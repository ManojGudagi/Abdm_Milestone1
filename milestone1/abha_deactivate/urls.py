from django.urls import path
from .views.deactivate_view import (
    GenerateDeactivateOtpView,
    VerifyDeactivateOtpView
)

urlpatterns = [
    path('deactivate/generate-otp/', GenerateDeactivateOtpView.as_view(), name='deactivate-generate-otp'),
    path('deactivate/verify-otp/', VerifyDeactivateOtpView.as_view(), name='deactivate-verify-otp'),
]
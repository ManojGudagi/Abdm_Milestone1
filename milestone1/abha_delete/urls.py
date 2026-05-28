from django.urls import path

# ✅ Use a single dot to look inside the local 'views' folder
from .views.delete_view import (
    GenerateDeleteOtpView,
    VerifyDeleteOtpView
)

urlpatterns = [
    path('delete/generate-otp/', GenerateDeleteOtpView.as_view(), name='delete-generate-otp'),
    path('delete/verify-otp/', VerifyDeleteOtpView.as_view(), name='delete-verify-otp'),
]
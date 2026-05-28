from django.urls import path
# ... your existing imports ...
from milestone1.abhanumber_recover.views.recovery_view import (
    GenerateRecoveryOtpView,
    VerifyRecoveryOtpView
)

urlpatterns = [
    # ... your existing paths ...
    
    # Forgot ABHA Recovery Routes
    path('recovery/generate-otp/', GenerateRecoveryOtpView.as_view(), name='recovery-generate-otp'),
    path('recovery/verify-otp/', VerifyRecoveryOtpView.as_view(), name='recovery-verify-otp'),
]
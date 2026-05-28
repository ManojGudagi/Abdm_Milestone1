# milestone1/enrollment_mobile/urls.py
from django.urls import path
from milestone1.email_verification.views.email_view import SendEmailVerificationView

urlpatterns = [

    # ✅ SEND EMAIL VERIFICATION LINK
    path("request/email/verification/", SendEmailVerificationView.as_view(), name="request-email-verification"),
    
]
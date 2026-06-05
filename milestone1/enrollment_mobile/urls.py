# milestone1/enrollment_mobile/urls.py

from django.urls import path
from django.views.generic import TemplateView # <-- ADD THIS IMPORT

from milestone1.enrollment_mobile.views.mobile_otp_view import (
    SendMobileOtpView,
    VerifyMobileOtpView
)

urlpatterns = [
    # --- ADD THIS BASE ROUTE TO SERVE THE HTML ---
    path('', TemplateView.as_view(template_name='mobile_enroll.html'), name='mobile-enroll-ui'),

    # ✅ SEND OTP
    path("request/mobile/otp/",SendMobileOtpView.as_view(),name="request-mobile-otp"),

    # ✅ VERIFY OTP
    path("verify/mobile/otp/",VerifyMobileOtpView.as_view(),name="verify-mobile-otp"),
]
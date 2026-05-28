# milestone1/enrollment_mobile/urls.py

from django.urls import path

from milestone1.enrollment_mobile.views.mobile_otp_view import (
    SendMobileOtpView,
    VerifyMobileOtpView
)


urlpatterns = [

    # ✅ SEND OTP
    path("request/mobile/otp/",SendMobileOtpView.as_view(),name="request-mobile-otp"),

    # ✅ VERIFY OTP
    path("verify/mobile/otp/",VerifyMobileOtpView.as_view(),name="verify-mobile-otp"),
]
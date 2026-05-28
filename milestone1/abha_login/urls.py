from django.urls import path
from milestone1.abha_login.views.login_views import (
    LoginRequestOtpView,
    LoginVerifyOtpView
)

urlpatterns = [
    # 🔐 STEP 1: Send OTP 
    path('profile/login/request/otp/', LoginRequestOtpView.as_view(), name='login-request-otp'),

    # 🔐 STEP 2: Verify OTP (Returns final Profile Token)
    path('profile/login/verify/otp/', LoginVerifyOtpView.as_view(), name='login-verify-otp'),
]
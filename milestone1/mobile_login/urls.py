from django.urls import path
# Import your mobile views...

from django.urls import path
from milestone1.mobile_login.views.login_views import (
    MobileRequestOtpView,
    MobileVerifyOtpView,
    MobileVerifyUserView
)

urlpatterns = [
    # ... your existing Aadhaar 2-step urls ...

    # 📱 MOBILE FLOW (3-Steps)
    path('mobile/login/request/otp/', MobileRequestOtpView.as_view(), name='mobile-request-otp'),
    path('mobile/login/verify/otp/', MobileVerifyOtpView.as_view(), name='mobile-verify-otp'),
    path('mobile/login/verify/user/', MobileVerifyUserView.as_view(), name='mobile-verify-user'),
]
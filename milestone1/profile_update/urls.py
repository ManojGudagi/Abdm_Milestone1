from django.urls import path
from milestone1.profile_update.views.profile_views import (
    ProfileRequestOtpView,
    ProfileVerifyView,
    ProfileEmailLinkView
)

urlpatterns = [
    # ⚙️ Unified Account Management Flow
    path('profile/account/request/otp/', ProfileRequestOtpView.as_view(), name='profile-request-otp'),
    path('profile/account/verify/', ProfileVerifyView.as_view(), name='profile-verify'),
    
    # 📧 Dedicated Email Flow
    path('profile/account/request/emailVerificationLink/', ProfileEmailLinkView.as_view(), name='profile-email-link'),
]
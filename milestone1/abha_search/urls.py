from django.urls import path
from milestone1.abha_search.views.login_views import (
    SearchAbhaView,
    SearchRequestOtpView,
    SearchVerifyOtpView
)

urlpatterns = [
    # 🔍 FIND ABHA FLOW (3-Steps)
    path('profile/account/abha/search/', SearchAbhaView.as_view(), name='search-abha'),
    path('profile/search/request/otp/', SearchRequestOtpView.as_view(), name='search-request-otp'),
    path('profile/search/verify/otp/', SearchVerifyOtpView.as_view(), name='search-verify-otp'),
]
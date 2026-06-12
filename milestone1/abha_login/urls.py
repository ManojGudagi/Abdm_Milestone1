from django.urls import path
from django.views.generic import TemplateView 

# --- Import Login Views ---
from milestone1.abha_login.views.login_views import (
    LoginRequestOtpView,
    LoginVerifyOtpView,
    profile_dashboard
)

# --- Import Search Views ---
from milestone1.abha_search.views.login_views import (
    SearchAbhaView,
    SearchRequestOtpView,
    SearchVerifyOtpView
)

urlpatterns = [
    # 🖥️ UI Route (Handles both Login and Search dynamically via JS):
    path('', TemplateView.as_view(template_name='abha_login.html'), name='abha-login-ui'),

    # ==========================================
    # =           LOGIN ROUTES                 =
    # ==========================================
    # 🔐 STEP 1: Send OTP 
    path('profile/login/request/otp/', LoginRequestOtpView.as_view(), name='login-request-otp'),
    
    # 🔐 STEP 2: Verify OTP (Returns final Profile Token)
    path('profile/login/verify/otp/', LoginVerifyOtpView.as_view(), name='login-verify-otp'),

    # ==========================================
    # =           SEARCH ROUTES                =
    # ==========================================
    # 🔍 STEP 1: Search Account
    path('profile/account/abha/search/', SearchAbhaView.as_view(), name='search-abha'),
    
    # 🔍 STEP 2: Request OTP
    path('profile/search/request/otp/', SearchRequestOtpView.as_view(), name='search-request-otp'),
    
    # 🔍 STEP 3: Verify OTP
    path('profile/search/verify/otp/', SearchVerifyOtpView.as_view(), name='search-verify-otp'),

    # ==========================================
    # =           DASHBOARD ROUTE              =
    # ==========================================
    path('portal/dashboard/', profile_dashboard, name='profile-dashboard'),
]
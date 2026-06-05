from django.urls import path
from django.views.generic import TemplateView # <-- ADD THIS IMPORT

from milestone1.enrollment_dl.views.dl_views import (
    DlSendOtpView,
    DlVerifyOtpView,
    DlDocumentVerifyView
)

urlpatterns = [
    # --- ADD THIS BASE ROUTE TO SERVE THE HTML ---
    path('', TemplateView.as_view(template_name='dl_enroll.html'), name='dl-enroll-ui'),

    # 🚗 STEP 1: Send OTP for Driving License
    path('dl/request/otp/', DlSendOtpView.as_view(), name='dl-request-otp'),
    # 🚗 STEP 2: Verify Mobile OTP
    path('dl/verify/otp/', DlVerifyOtpView.as_view(), name='dl-verify-otp'),
    # 🚗 STEP 3: Verify DL Document & Generate Profile
    path('dl/enrol/document/', DlDocumentVerifyView.as_view(), name='dl-verify-document'),
]
from django.urls import path

# Adjust this import path depending on where you saved your dl_views.py file!
from milestone1.enrollment_dl.views.dl_views import (
    DlSendOtpView,
    DlVerifyOtpView,
    DlDocumentVerifyView
)

urlpatterns = [
    # 🚗 STEP 1: Send OTP for Driving License
    path('dl/request/otp/', DlSendOtpView.as_view(), name='dl-request-otp'),

    # 🚗 STEP 2: Verify Mobile OTP
    path('dl/verify/otp/', DlVerifyOtpView.as_view(), name='dl-verify-otp'),

    # 🚗 STEP 3: Verify DL Document & Generate Profile
    path('dl/enrol/document/', DlDocumentVerifyView.as_view(), name='dl-verify-document'),
]
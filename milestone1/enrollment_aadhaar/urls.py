# milestone1/enrollment_aadhaar/urls.py

from django.urls import path
from milestone1.enrollment_aadhaar.views.otp_view import AadhaarOtpVerifyView, AadhaarOtpView, SendOtpView
from milestone1.enrollment_aadhaar.views.auth_view import CertificateView, SessionTokenView
from milestone1.enrollment_aadhaar.views.encryption_view import EncodeDataView
from milestone1.enrollment_aadhaar.views.enrol_view import ABHAProfileView, AadhaarEnrolView, DownloadProfileView
from milestone1.email_verification.views.email_view import SendEmailVerificationView

urlpatterns = [
    # path('generate-otp/', AadhaarOtpView.as_view(), name='generate-otp'),
    path('sessions/', SessionTokenView.as_view(), name='sessions'),
    path('certificate/', CertificateView.as_view(), name='certificate'),
    path('verify-otp/', AadhaarOtpVerifyView.as_view(),name='verify-otp'),
   # path("encode/", EncodeDataView.as_view(),name="encode-data"),
    path("send-otp/", SendOtpView.as_view(), name="send-otp"),
    path('enrol/', AadhaarEnrolView.as_view()),
    path('get-profile/',ABHAProfileView.as_view(),name='get-profile'),
    path('download-abha-card/', DownloadProfileView.as_view(), name='download-abha-card'),
    path("request/email/verification/", SendEmailVerificationView.as_view(), name="request-email-verification"),
]
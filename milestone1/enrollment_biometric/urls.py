from django.urls import path

# Adjust this import path depending on where you saved your biometric_views.py file!
from milestone1.enrollment_biometric.views.biometric_views import (
    FaceAuthInitView,
    FaceAuthStatusView,
    BiometricEnrolView
)

urlpatterns = [
    # ==========================================
    # 📸 FACE AUTH FLOW (3 Steps)
    # ==========================================
    # 📸 STEP 1: Init Transaction (Generates the QR Code txnId)
    path('biometric/face/init/', FaceAuthInitView.as_view(), name='face-auth-init'),

    # 📸 STEP 2: Polling Status (Check if user completed the face scan)
    path('biometric/face/status/', FaceAuthStatusView.as_view(), name='face-auth-status'),


    # ==========================================
    # 👆 👁️ 📸 UNIFIED VERIFICATION
    # ==========================================
    # 🎯 STEP 3 for Face Auth 
    # 🎯 STEP 1 for Fingerprint & Iris (They skip straight here!)
    path('biometric/verify/', BiometricEnrolView.as_view(), name='biometric-verify'),
]